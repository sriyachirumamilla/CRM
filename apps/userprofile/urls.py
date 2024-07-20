# apps/userprofile/urls.py

from django.urls import path
from .views import ProfileUpdateView
from apps.common.views import DashboardView
urlpatterns = [
    path('profile/update/', ProfileUpdateView.as_view(), name='profile-update'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    
]
