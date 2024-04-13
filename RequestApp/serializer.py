from rest_framework import serializers
from .models import Request, Report , Notification
from CommunityApp.views import create_club
from PostApp.views import post_detail
from CommunityApp.views import *
class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ['id', 'description','student','post','club','event']
 
class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['id', 'user','post','status']
        read_only_field = ['user','post']
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'