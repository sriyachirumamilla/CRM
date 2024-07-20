from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView

from apps.common.models import UserProfile
from .forms import LoginForm, SignUpForm, UserForm, ProfileForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib import messages
#from apps.userprofile.models import UserProfile

class HomeView(TemplateView):
    template_name = 'common/home.html'


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'common/dashboard.html'
    login_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['companies_count'] = UserProfile.objects.count()
        context['contacts_count'] = User.objects.count()

        context['recent_activities'] = [
            'Contact John Doe added.',
            'Company ABC Corp updated.',
            'Meeting scheduled with Jane Smith.',
        ]

        # Example CRM info
        context['crm_info_1'] = "CRM Info 1 Value"  # Replace with actual data
        context['crm_info_2'] = "CRM Info 2 Value"  # Replace with actual data
        context['crm_info_3'] = "CRM Info 3 Value"  # Replace with actual data

        return context



class SignUpView(View):
    def get(self, request):
        form = SignUpForm()
        return render(request, 'common/register.html', {'form': form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            return redirect('login')
        return render(request, 'common/register.html', {'form': form})


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'common/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class ProfileUpdateView(LoginRequiredMixin, TemplateView):
    user_form = UserForm
    profile_form = ProfileForm
    template_name = 'common/profile-update.html'

    def post(self, request):
        post_data = request.POST or None
        file_data = request.FILES or None

        user_form = UserForm(post_data, instance=request.user)
        profile_form = ProfileForm(post_data, file_data, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully!')
            return HttpResponseRedirect(reverse_lazy('profile'))

        context = self.get_context_data(
            user_form=user_form,
            profile_form=profile_form
        )
        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


def facebook_login_redirect(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        return redirect('dashboard')

from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            return redirect('dashboard')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def profile(request):
    user = request.user
    print(user)  # Check user object
    print(user.profile)  # Check profile object
    
    context = {
        'user': user,
    }
    return render(request, 'profile.html', context)

