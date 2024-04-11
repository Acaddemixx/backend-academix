from rest_framework import serializers
from .models import Department, Course, Building


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['head', 'name', 'overview']

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['name', 'deparment', 'academic_year', 'semester', 'credit_hr', 'lecture_hr', 'overview']

class BuildingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Building
        fields = ['name', 'block_number', 'tyoe', 'description']
