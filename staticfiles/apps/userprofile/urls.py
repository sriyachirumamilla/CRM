# userprofile/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    # Add more paths as needed
]
