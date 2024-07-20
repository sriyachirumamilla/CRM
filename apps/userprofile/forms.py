# apps/userprofile/forms.py

from django import forms
from .models import UserProfile, Profile

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'location', 'birth_date']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'website', 'phone_number']
