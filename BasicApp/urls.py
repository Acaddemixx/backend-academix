from django.urls import path
from . import views

urlpatterns = [
    path('departments/', views.create_or_get_department, name='create_department'),
    path('departments/<int:id>', views.department_detail, name='get_department'),
    path('courses/', views.create_or_get_course, name='create_course'),
    path('courses/<int:id>', views.course_detail, name='create_detail'),
    path('building/', views.create_or_get_building, name='create_or_get_building'),
    path('building/<int:id>', views.building_detail, name='building_detail')
]