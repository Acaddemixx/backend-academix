from django.db import models
from BasicApp.models import Building
from UserApp.models import Student
from pgvector.django import VectorField
from AI import main
# Create your models here.

class Club(models.Model):
    name = models.CharField(max_length = 50)
    overview = models.TextField()
    founder = models.OneToOneField(Student)
    member = models.ManyToManyField(Student)

    def set_embedding(self):
        text = f"Club named: {self.name}, overview: {self.overview}"
        vector_text = main.embed(text)
        self.embedding = vector_text

    def save(self, *args, **kwargs):
        self.set_embeddingg()
        super().save(*args, **kwargs)

class Section(models.Model):
    name = models.CharField(max_length = 50)
    rep = models.OneToOneField(Student)

class Event(models.Model):
    building = models.OneToOneField(Building)
    club = models.ForeignKey(Club)
    start_time = models.DateField()
    end_time = models.DateField()
    description = models.TextField()
    embedding = VectorField(dimensions= 768 , null = True , blank = True)

    def set_embedding(self):
        text = f"Event starting at: {self.start_time}, description: {self.description}"
        vector_text = main.embed(text)
        self.embedding = vector_text

    def save(self, *args, **kwargs):
        self.set_embeddingg()
        super().save(*args, **kwargs)







