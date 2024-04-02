from django.db import models
from pgvector.django import VectorField
from AI import main
# Create your models here.
class Post(models.Model):
    author = models.ForeignKey('UserApp.Student', on_delete=models.SET_NULL)
    club = models.ForeignKey('CommunityApp.Club', null=True, on_delete=models.SET_NULL)
    section = models.ForeignKey('CommunityApp.Section', null=True, on_delete=models.SET_NULL)
    course = models.ForeignKey('CommunityApp.Section', null=True, on_delete=models.SET_NULL)
    created_at = models.DateField(auto_now_add=True)
    content = models.TextField()
    #file field pic or pdf 

    embedding = VectorField(dimensions= 768 , null = True , blank = True)

    def set_embedding(self):
        text = f"Post Author: {self.author.first_name}, content: {self.content}"
        vector_text = main.embed(text)
        self.embedding = vector_text

    def save(self, *args, **kwargs):
        self.set_embeddingg()
        super().save(*args, **kwargs)
        
    def __str__(self) -> str:
        return self.created_at

class Comment(models.Model):
    content = models.TextField()
    user = models.ForeignKey('UserApp.Student', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    embedding = VectorField(dimensions= 768 , null = True , blank = True)

    def set_embedding(self):
        text = f"User comment content: {self.content}, made by: {self.user.first_name}"
        vector_text = main.embed(text)
        self.embedding = vector_text

    def save(self, *args, **kwargs):
        self.set_embeddingg()
        super().save(*args, **kwargs)
        
    def __str__(self) -> str:
        return self.content

class Like(models.Model):
    user = models.ForeignKey('UserApp.Student', on_delete=models.SET_NULL)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.user.first_name