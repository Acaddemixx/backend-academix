from rest_framework import serializers
from .models import Student, Admin
import re

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'username', 'first_name', 'last_name', 'phone_number', 'email', 'student_id', 'is_student', 'academic_year', 'password']
    
    def validate_student_id(self, value):
        if not re.match('[a-zA-Z]{3}[0-9]{4}\/[0-9]{2}', value):
            raise serializers.ValidationError('school id wrong eg. ETS0333/14')
        return value

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = ['username', 'first_name', 'last_name', 'phone_number', 'email', 'student_id', 'is_admin', 'academic_year', 'password']
