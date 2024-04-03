from django.db import models
from UserApp.models import Admin
from pgvector.django import VectorField
from AI import main
# Create your models here.

class Department(models.Model):
    head = models.OneToOneField(Admin) 
    name = models.CharField(max_length = 50)
    overview = models.TextField()
    embedding = VectorField(dimensions= 768 , null = True , blank = True)

    def set_embedding(self):
        text = f"Department name: {self.name}, overview: {self.overview}"
        vector_text = main.embed(text)
        self.embedding = vector_text

    def save(self, *args, **kwargs):
        self.set_embeddingg()
        super().save(*args, **kwargs)

class Course(models.Model):
    name = models.CharField(max_length = 50)
    department = models.ManyToManyField(Department)
    academic_year = models.DateField()
    semester = models.IntegerField()
    credit_hour = models.IntegerField()
    lecture_hour = models.IntegerField()
    overview = models.TextField()
    embedding = VectorField(dimensions= 768 , null = True , blank = True)

    def set_embedding(self):
        text = f"Course name: {self.name}, overview: {self.overview}"
        vector_text = main.embed(text)
        self.embedding = vector_text

    def save(self, *args, **kwargs):
        self.set_embeddingg()
        super().save(*args, **kwargs)

class Building(models.Model):
    name = models.CharField()
    block_number = models.IntegerField()
    type = models.CharField(max_length = 50)
    description = models.TextField()
    #vector field comming
    embedding = VectorField(dimensions= 768 , null = True , blank = True)
    
    def set_embedding(self):
        text = f"Building name: {self.name}, Description: {self.description} , block number: {self.block_number} , type: {self.type}"
        vector_text = main.embed(text)
        self.embedding = vector_text

    def save(self, *args, **kwargs):
        self.set_embeddingg()
        super().save(*args, **kwargs)
    




