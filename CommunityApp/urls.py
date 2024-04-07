from django.urls import path
from . import views


urlpatterns = [
    path('club/',views.get_all_clubs , name = 'display-all-clubs'),
    path('club/<int:id>', views.get_club , name = 'display-club'),
    path('club/<int:id>/related' , views.get_related_club , name = 'display-related-clubs'),
    path('club/create' , views.create_club , name = 'create-club'),
    path('club/<int:id>/update' , views.update_club , name = 'update-club'),
    path('club/<int:id>/delete' , views.delete_club , name= 'delete-club'),

    path('section/' , views.get_all_section , name = 'display-all-sections'),
    path('section/<int:id>', views.get_section , name='display-section'),
    path('section/create' , views.create_section , name = 'create-section'),
    path('section/<int:id>/update' , views.update_section , name='update-section'),
    path('section/<int:id>/delete', views.delete_section , name='delete-section'),
    
    path('event/', views.get_all_events , name='display-all-events'),
    path('event/<int:id>', views.get_event , name = 'display-event'),
    path('event/<int:id>/related' , views.get_related_events , name = 'display-related-events'),
    path('event/<int:id>/update' , views.update_event , name='update-event'),
    path('event/<int:id>/delete' , views.delete_event , name = 'delete-event'),
]