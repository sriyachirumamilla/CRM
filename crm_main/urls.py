# crm_main/urls.py

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from apps.common.views import CompaniesView, home, SignUpView, DashboardView, ProfileUpdateView, ProfileView, FacebookLogin, change_password_view, contacts_view, sales_view
from django.contrib.auth import views as auth_views
from apps.common import views as common_views
from apps.common.views import DashboardView
from apps.common.views import CustomLoginView, home, DashboardView, facebook_login_redirect
from apps.common import apps
# from crm_main.apps.userprofile.views import dashboard_view
# from crm_main.apps.common import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.common.urls')),
    path('userprofile/', include('apps.userprofile.urls')),
    path('oauth/', include('social_django.urls', namespace='unique_social')),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    #path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('facebook/login/token/', FacebookLogin.as_view(), name='facebook_login'),
    path('facebook-login/', common_views.facebook_login_redirect, name='facebook_login_redirect'),
    path('profile-update/', ProfileUpdateView.as_view(), name='profile-update'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('register/', SignUpView.as_view(), name="register"),
    path('accounts/', include('allauth.urls')),
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),
    path('facebook-login/', facebook_login_redirect, name='facebook_login_redirect'),
    #path('auth/facebook/', FacebookLogin.as_view(), name='fb_login'),
    #path('login/', CustomLoginView.as_view(template_name='common/login.html'), name='login'),
   path('login/', auth_views.LoginView.as_view(template_name='common/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('change_password/', change_password_view, name='change_password'),
    path('sales/', sales_view, name='sales'),
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='common/password-reset/password_reset.html',
             subject_template_name='common/password-reset/password_reset_subject.txt',
             email_template_name='common/password-reset/password_reset_email.html',
             # success_url='/login/'
         ),
         name='password_reset'
    ),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='common/password-reset/password_reset_done.html'
         ),
         name='password_reset_done'
    ),
    path('', include('apps.common.urls')),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='common/password-reset/password_reset_confirm.html'
         ),
         name='password_reset_confirm'
    ),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='common/password-reset/password_reset_complete.html'
         ),
         name='password_reset_complete'
    ),
    path('change-password/', auth_views.PasswordChangeView.as_view(
            template_name='common/change-password.html',
            success_url='/'
        ),
        name='change-password'
    ),
    path('companies/', CompaniesView.as_view(), name='companies'),
    path('contacts/', contacts_view, name='contacts'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
