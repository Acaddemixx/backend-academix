from django.db import models
from UserApp.models import Admin

# Create your models here.

class Department(models.Model):
    head = models.OneToOneField(Admin) 
    name = models.CharField(max_length = 50)
    overview = models.TextField()
    #vector field comming

class Course(models.Model):
    name = models.CharField(max_length = 50)
    department = models.ManyToManyField(Department)
    academic_year = models.DateField()
    semester = models.IntegerField()
    credit_hour = models.IntegerField()
    lecture_hour = models.IntegerField()
    overview = models.TextField()
    #vector field comming

class Building(models.Model):
    name = models.CharField()
    block_number = models.IntegerField()
    type = models.CharField(max_length = 50)
    description = models.TextField()
    #vector field comming

    




