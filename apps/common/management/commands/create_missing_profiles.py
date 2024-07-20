from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.userprofile.models import UserProfile, Profile

class Command(BaseCommand):
    help = 'Create missing UserProfile and Profile objects for users'

    def handle(self, *args, **kwargs):
        users_without_userprofile = User.objects.filter(common_userprofile__isnull=True)
        for user in users_without_userprofile:
            UserProfile.objects.create(user=user)
        
        users_without_profile = User.objects.filter(common_profile__isnull=True)
        for user in users_without_profile:
            Profile.objects.create(user=user)
        
        self.stdout.write(self.style.SUCCESS('Successfully created missing UserProfile and Profile for users'))
