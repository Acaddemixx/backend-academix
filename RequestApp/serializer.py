from rest_framework import serializers
from .models import Request, Report
from CommunityApp.views import create_club
from PostApp.views import create_requested_post
from CommunityApp.views import create_event
class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ['description','status','student','post','club','event']
        read_only_field = ['student','club']
    def create(self, validated_data):
        validated_data['status'] = 3  
        return super().create(validated_data)
    def update(self,request, validated_data):
        if request.user.is_staff:
            approved_data = validated_data.get('status')
            if approved_data == 1:
                validated_data['status'] = 1
                if self.club:
                    create_club(request)
                elif self.post:
                    create_requested_post(request)
                elif self.event:
                    create_event(request)
            elif approved_data == 2:
                validated_data['status'] = 2
            return super().update(validated_data)
        else:
            return super().create(validated_data)
            
       
class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['user','post','status']
        read_only_field = ['user','post']
    def create(self, validated_data):
        validated_data['status'] = 3 
        return super().create(validated_data)
    
    def update(self,request, validated_data):
        if request.user.is_satff:
            approved_data = validated_data.get('status')
            if approved_data == 1:
                validated_data['status'] = 1
            return super().create(validated_data)
        else:
            return super().create(validated_data)