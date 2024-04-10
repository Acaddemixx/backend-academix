from django.urls import path
from .import views

urlpatterns = [
      path('request/create',views.create_request , name = 'create-request'),
      path('request/<int:id>/update', views.edit_request, name='edit-request'),
      path('request/<int:id>/accepted',views.get_accepted_requests, name='get-accepted-request'),
      path('request/<int:id>/denied',views.get_denied_requests, name='get-denied-request'),
      path('request/<int:id>/pending',views.get_pending_requests, name='get-pending-request'),
      path('request/<int:id>/accepted',views.get_accepted_requests, name='get-accepted-request'),
      path('request/all',views.get_all_requests, name='get-all-request'),
      path('request/<int:id>/delete',views.delete_request, name='delete-request'),
      path('report/create',views.create_report, name='create-report'),
      path('report/<int:id>/edit',views.edit_report, name='edit-report'),
      path('report/pending',views.get_pending_report, name='get-pending-report'),
      path('report/all',views.get_all_report, name='get-all-report'),
      path('report/<int:id>/delete',views.delete_report, name='delete-report'),
]