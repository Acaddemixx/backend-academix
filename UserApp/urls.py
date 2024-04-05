from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.signUp, name='student-sign-up'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('test/', views.test_token, name='test-token')
]