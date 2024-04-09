from django.db import models
from UserApp.models import Student
from CommunityApp.models import Club,Event


# Create your models here.

class Request(models.Model):
    description = models.TextField()
    status = models.IntegerField()
    student = models.OneToOneField('UserApp.Student', on_delete=models.CASCADE, related_name='student_request') ###
    post = models.OneToOneField('UserApp.Student', null = True, on_delete=models.SET_NULL)
    club = models.OneToOneField('CommunityApp.Club', null = True, on_delete=models.SET_NULL)
    event = models.OneToOneField('CommunityApp.Event', null = True, on_delete=models.SET_NULL)

class Report(models.Model):
    status = models.IntegerField()
    user = models.OneToOneField('UserApp.Student', on_delete=models.CASCADE) ##
    post = models.OneToOneField('PostApp.Post', on_delete=models.CASCADE) ##
