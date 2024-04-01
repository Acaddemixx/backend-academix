from django.db import models
from BasicApp.models import Building
from UserApp.models import Student
# Create your models here.

class Club(models.Model):
    name = models.CharField(max_length = 50)
    overview = models.TextField()
    founder = models.OneToOneField(Student)
    member = models.ManyToManyField(Student)

class Section(models.Model):
    name = models.CharField(max_length = 50)
    rep = models.OneToOneField(Student)

class Event(models.Model):
    building = models.OneToOneField(Building)
    club = models.ForeignKey(Club)
    start_time = models.DateField()
    end_time = models.DateField()







