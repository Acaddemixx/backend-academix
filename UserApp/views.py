from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from .serializer import StudentSerializer, AdminSerializer, MyUserSerializer
from .models import Student, Admin, MyUser
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication


@api_view(['POST'])
def signUp(request):
    '''student signup route'''

    fields = set(['student_id', 'academic_year', 'semester', 'department', 'section'])

    hashmap = {key: value for key, value in request.data.items() if key not in fields}
    newMap = {key: value for key, value in request.data.items() if key in fields}

    serializer = MyUserSerializer(data=hashmap)
    student = StudentSerializer(data=newMap)

    if serializer.is_valid() and student.is_valid():
        user = serializer.save()
        student1 = student.save()
        user.set_password(request.data['password'])
        user.student = student1
        user.save()
        if not Student.objects.filter(section=user.student.section):
            user.student.is_rep = True
            user.student.save()
        serializer = MyUserSerializer(instance=user)
        serializer_copy = serializer.data.copy()
        serializer_copy['student'] = StudentSerializer(instance=student1).data
        token = Token.objects.create(user=user)

        return Response({"Token": token.key, "user": serializer_copy}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    '''student and admin login route'''

    username = request.data['username']
    password = request.data['password']

    user = MyUser.objects.filter(username=username).first()
    if user and user.check_password(password):
        serializer = MyUserSerializer(instance=user)
        token, create = Token.objects.get_or_create(user=user)
        serializer_copy = serializer.data

        if user.is_staff:
            serializer_copy['admin'] = AdminSerializer(instance=user.admin).data
        else:
            serializer_copy['student'] = StudentSerializer(instance=user.student).data
        
        return Response({"Token": token.key, "user": serializer_copy}, status=status.HTTP_201_CREATED)
    return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def test_token(request):
    '''token tester'''
    return Response(f"pass {request.user.student.student_id}", status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    '''logout route'''

    Token.objects.filter(user=request.user).delete()
    return Response("successfully logged out", status=status.HTTP_200_OK)
