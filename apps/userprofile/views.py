from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import View
from django.http import HttpResponseRedirect
from django.contrib import messages

from .forms import UserUpdateForm, ProfileUpdateForm
from .models import UserProfile, Profile

class ProfileUpdateView(LoginRequiredMixin, View):
    user_form = UserUpdateForm
    profile_form = ProfileUpdateForm
    template_name = 'userprofile/profile-update.html'

    def post(self, request):
        post_data = request.POST or None
        file_data = request.FILES or None

        # Handle the case where related objects might not exist
        try:
            user_profile = request.user.common_userprofile
        except UserProfile.DoesNotExist:
            user_profile = UserProfile.objects.create(user=request.user)

        try:
            common_profile = request.user.common_profile
        except Profile.DoesNotExist:
            common_profile = Profile.objects.create(user=request.user)

        user_form = UserUpdateForm(post_data, instance=user_profile)
        profile_form = ProfileUpdateForm(post_data, file_data, instance=common_profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully!')
            return HttpResponseRedirect(reverse_lazy('profile'))

        context = self.get_context_data(
            user_form=user_form,
            profile_form=profile_form
        )
        return render(request, self.template_name, context)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
