from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from .serializer import StudentSerializer, AdminSerializer
from .models import Student, Admin
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication


@api_view(['POST'])
def signUp(request):
    serializer = StudentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        student = Student.objects.get(username=request.data['username'])
        student.set_password(request.data['password'])
        student.is_student = True
        student.save()
        serializer = StudentSerializer(instance=student)
        token = Token.objects.create(user=student)

        return Response({"Token": token.key, "student": serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    username = request.data['username']
    password = request.data['password']

    student = Student.objects.get(username=username)
    if student and student.check_password(password):
        serializer = StudentSerializer(instance=student)
        token, create = Token.objects.get_or_create(user=student)
        return Response({"Token": token.key, "student": serializer.data}, status=status.HTTP_201_CREATED)

    admin = Admin.objects.get(username=username)
    if admin and admin.check_password(password):
        serializer = AdminSerializer(instance=admin)
        token, create = Token.objects.get_or_create(user=admin)
        return Response({"Token": token.key, "admin": serializer.data}, status=status.HTTP_201_CREATED)
    return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response(f"pass {request.user.student_id}", status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    Token.objects.filter(user=request.user).delete()
    return Response("successfully logged out", status=status.HTTP_200_OK)
