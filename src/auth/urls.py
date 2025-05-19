from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from .views import custom_logout

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('logout/', custom_logout, name='logout'),
]