from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.contrib import messages
import json

from .models import UserProfile, Profile, Company, Contact, SalesReport, Product
from .forms import SignUpForm, UserForm, ProfileForm, UserProfileForm
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from django.contrib.auth.views import LoginView

class CustomPasswordChangeView(PasswordChangeView):
    success_url = reverse_lazy('dashboard')

def change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'common/change-password.html', {'form': form})

from django.shortcuts import render

def home(request):
    return render(request, 'common/home.html')

class DashboardView(TemplateView):
    template_name = 'common/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['companies_count'] = Company.objects.count()
        context['contacts_count'] = Contact.objects.count()
        context['recent_activities'] = [
            'Contact John Doe added.',
            'Company ABC Corp updated.',
            'Meeting scheduled with Jane Smith.',
        ]
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

class ProfileUpdateView(LoginRequiredMixin, View):
    user_form = UserForm
    profile_form = ProfileForm
    user_profile_form = UserProfileForm
    template_name = 'common/profile-update.html'

    def post(self, request):
        post_data = request.POST or None
        file_data = request.FILES or None

        user_form = UserForm(post_data, instance=request.user)
        profile_form = ProfileForm(post_data, file_data, instance=request.user.common_profile)
        user_profile_form = UserProfileForm(post_data, instance=request.user.common_userprofile)

        if user_form.is_valid() and profile_form.is_valid() and user_profile_form.is_valid():
            user_form.save()
            profile_form.save()
            user_profile_form.save()
            messages.success(request, 'Your profile is updated successfully!')
            return HttpResponseRedirect(reverse_lazy('profile'))

        context = self.get_context_data(
            user_form=user_form,
            profile_form=profile_form,
            user_profile_form=user_profile_form,
        )
        return render(request, self.template_name, context)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

def facebook_login_redirect(request):
    if request.user.is_authenticated:
        return redirect('sales')
    else:
        return redirect('login')

class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter

class CompaniesView(View):
    def get(self, request):
        companies = Company.objects.all()
        return render(request, 'common/companies.html', {'companies': companies})

def contacts_view(request):
    contacts = Contact.objects.all()
    return render(request, 'common/contacts.html', {'contacts': contacts})

# common/views.py
from django.shortcuts import render
import json
from .models import SalesReport

def sales(request):
    sales_data = SalesReport.objects.all()

    if not sales_data.exists():
        return render(request, 'common/sales.html', {'message': 'No sales data available.'})

    sales_data_for_chart = [{'month_name': entry.month_name, 'sales': entry.sales} for entry in sales_data]

    return render(request, 'common/sales.html', {
        'sales_data': json.dumps(sales_data_for_chart)
    })
# common/views.py
from django.shortcuts import render
import json

def sales_view(request):
    sales_data = SalesReport.objects.all()

    if not sales_data.exists():
        return render(request, 'common/sales.html', {'message': 'No sales data available.'})

    # Prepare data for chart
    sales_data_for_chart = [{'month_name': entry.month_name, 'sales': entry.sales} for entry in sales_data]

    return render(request, 'common/sales.html', {
        'sales_data_json': json.dumps(sales_data_for_chart)
    })


def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

class CustomLoginView(LoginView):
    def get_success_url(self):
        return reverse_lazy('sales')
