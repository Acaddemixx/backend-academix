from rest_framework import serializers
from .models import Post, Comment, Like
from RequestApp.models import Request

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'author', 'created_at', 'content', 'file', 'section', 'club']
        read_only_fields = ['created_at', 'author', 'section', 'club']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['likes'] = Like.objects.filter(post_id= instance.id).count()
        return ret

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'user', 'content', 'post']
        read_only_fields = ['post', 'user']

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['user', 'post']
