from django.urls import path
from .import views

urlpatterns = [
      path('request/create',views.create_request , name = 'create-request'),
      path('request/<int:id>/update', views.edit_request, name='edit-request'),
      path('request/<int:id>/accepted',views.get_accepted_requests, name='get-accepted-request'),
      path('')
]