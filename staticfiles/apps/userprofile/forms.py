from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['user', 'website', 'avatar', 'phone_number']  # Adjust fields as per your model
