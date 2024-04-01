from django.db import models
from django.contrib.auth.models import AbstractUser
from CommunityApp.models import Section
from BasicApp.models import Department
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
    is_rep = models.BooleanField()
    section = models.ForeignKey(Section)
    department = models.ForeignKey(Department)

class Admin(MyUser):
    department = models.ForeignKey(Department)


    









