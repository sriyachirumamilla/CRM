# userprofile/views.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import UserProfile, Profile

@login_required
def profile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    profile = Profile.objects.get(user=request.user)
    context = {
        'user_profile': user_profile,
        'profile': profile,
    }
    return render(request, 'userprofile/profile.html', context)
