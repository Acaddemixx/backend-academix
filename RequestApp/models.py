from django.db import models
from UserApp.models import Student
from CommunityApp.models import Club,Event


# Create your models here.

class Request(models.Model):
    description = models.TextField()
    student = models.OneToOneField(Student)
    post = models.OneToOneField(Student , null = True)
    club = models.OneToOneField(Club , null = True)
    event = models.OneToOneField(Event, null = True)

class Report(models.Model):
    user = models.OneToOneField()
    post = models.OneToOneField()



