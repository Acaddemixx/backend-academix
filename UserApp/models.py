from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group, Permission
# Create your models here.


class MyUser(AbstractUser):
    first_name = models.CharField()
    last_name = models.CharField()
    phone_number = models.CharField()
    email = models.CharField()
    class Meta:
        abstract = True

class Student(MyUser):
    student_id = models.CharField()
    academic_year = models.DateField()
    is_rep = models.BooleanField(null=True)
    section = models.ForeignKey('CommunityApp.Section', null=True, on_delete=models.SET_NULL, related_name='student')##
    department = models.ForeignKey('BasicApp.Department', null=True, on_delete=models.CASCADE, related_name='student') ##
    groups = models.ManyToManyField(Group, related_name='student_users')
    user_permissions = models.ManyToManyField(Permission, related_name='student_users_permissions')

class Admin(MyUser):
    department = models.ForeignKey('BasicApp.Department', on_delete=models.CASCADE, related_name='admin') ##
    groups = models.ManyToManyField(Group, related_name='admin_users')
    user_permissions = models.ManyToManyField(Permission, related_name='admin_users_permissions')
