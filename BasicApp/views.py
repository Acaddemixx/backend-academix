from rest_framework.decorators import api_view, permission_classes
from .serializer import DepartmentSerializer, CourseSerializer, BuildingSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import Department, Course, Building
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

'''department routes'''

@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def create_or_get_department(request):
    '''getting all department objects or creating deparment object'''

    if request.method == 'POST':
        serializer = DepartmentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        departements = Department.objects.all()
        serializer = DepartmentSerializer(departements, many=True)

        return Response({"department": serializer.data}, status=status.HTTP_200_OK)


@api_view(['PUT', 'GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def department_detail(request, id):
    '''getting , deleteing or updating deparment object'''

    if request.method == 'GET':
        department = get_object_or_404(Department, id=id)
        serializer = DepartmentSerializer(instance=department)

        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        department = get_object_or_404(Department, id=id)
        department.delete()

        return Response("deleted succesfully", status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        department = get_object_or_404(Department, id=id)
        serializer = DepartmentSerializer(department, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)


'''course routes'''


@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def create_or_get_course(request):
    '''getting all course objects or creating course object'''

    if request.method == 'POST':
        serializer = CourseSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        course = course.objects.all()
        serializer = CourseSerializer(course, many=True)

        return Response({"course": serializer.data}, status=status.HTTP_200_OK)


@api_view(['PUT', 'GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def course_detail(request, id):
    '''getting , deleteing or updating course object'''

    if request.method == 'GET':
        course = get_object_or_404(Course, id=id)
        serializer = CourseSerializer(instance=course)

        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        course = get_object_or_404(Course, id=id)
        course.delete()

        return Response("deleted succesfully", status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        course = get_object_or_404(Course, id=id)
        serializer = CourseSerializer(course, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

'''building routes'''

@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def create_or_get_building(request):
    '''getting all course objects or creating building object'''

    if request.method == 'POST':
        serializer = BuildingSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        building = Building.objects.all()
        serializer = BuildingSerializer(building, many=True)

        return Response({"buildings": serializer.data}, status=status.HTTP_200_OK)


@api_view(['PUT', 'GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def building_detail(request, id):
    '''getting , deleteing or updating course object'''

    if request.method == 'GET':
        building = get_object_or_404(Building, id=id)
        serializer = BuildingSerializer(instance=building)

        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        building = get_object_or_404(Building, id=id)
        building.delete()

        return Response("deleted succesfully", status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        building = get_object_or_404(Building, id=id)
        serializer = CourseSerializer(Building, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def year_courses(request):
    department = get_object_or_404(Department , id = request.data['department'])
    year = request.data['year']

    courses = Course.objects.filter(department= department , academic_year = year)
    serializer = CourseSerializer(courses , many = True)

    return Response(serializer.data, status=status.HTTP_200_OK)




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def semester_courses(request , department , course , year , semester):
    department = get_object_or_404(Department , id = department)
    semester = semester
    year = year
    print(semester = semester)

    courses = Course.objects.filter(department= department , semester = semester , year= year)
    serializer = CourseSerializer(courses , many = True)

    return Response(serializer.data, status=status.HTTP_200_OK)


