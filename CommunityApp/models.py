from django.db import models

class Club(models.Model):
    name = models.CharField(max_length = 50)
    overview = models.TextField()
    founder = models.OneToOneField('UserApp.Student', null=True, on_delete=models.SET_NULL, related_name='club_founder')
    members = models.ManyToManyField('UserApp.Student')

class Section(models.Model):
    name = models.CharField(max_length = 50)
    rep = models.OneToOneField('UserApp.Student', null=True, on_delete=models.SET_NULL, related_name='representative')

class Event(models.Model):
    building = models.OneToOneField('BasicApp.Building', null=True, on_delete=models.SET_NULL) #####
    club = models.ForeignKey(Club, on_delete=models.CASCADE)#####
    start_time = models.DateField()
    end_time = models.DateField()
