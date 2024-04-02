from django.db import models

class Post(models.Model):
    author = models.ForeignKey('UserApp.Student', null=True, on_delete=models.SET_NULL)
    club = models.ForeignKey('CommunityApp.Club', null=True, on_delete=models.SET_NULL)
    section = models.ForeignKey('CommunityApp.Section', null=True, on_delete=models.SET_NULL, related_name='section_posts')
    course = models.ForeignKey('CommunityApp.Section', null=True, on_delete=models.SET_NULL, related_name='course_posts')
    created_at = models.DateField(auto_now_add=True)

class Comment(models.Model):
    content = models.TextField()
    user = models.ForeignKey('UserApp.Student', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class Like(models.Model):
    user = models.ForeignKey('UserApp.Student', null=True, on_delete=models.SET_NULL)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
