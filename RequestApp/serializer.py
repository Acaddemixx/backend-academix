from rest_framework import serializers
from .models import Request, Report
from CommunityApp.views import create_club
from PostApp.views import post_detail
from CommunityApp.views import *
class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ['description','student','post','club','event']
 
class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['user','post','status']
        read_only_field = ['user','post']
