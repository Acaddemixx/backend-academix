from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from .serializer import StudentSerializer
from .models import Student
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
        student.save()
        token = Token.objects.create(user=student)

        return Response({"Token": token.key, "student": serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    student = get_object_or_404(Student, username=request.data['username'])
    if not student.check_password(request.data['password']):
        return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)
    serializer = StudentSerializer(instance=student)
    token, create = Token.objects.get_or_create(user=student)
    return Response({"Token": token.key, "student": serializer.data}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response(f"pass {request.user.student_id}", status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    Token.objects.filter(user=request.user).delete()
    return Response("successfully logged out", status=status.HTTP_200_OK)
