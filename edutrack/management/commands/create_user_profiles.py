from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import UserProfile

class Command(BaseCommand):
    help = 'Creates UserProfile for all existing users'

    def handle(self, *args, **options):
        users_without_profiles = User.objects.filter(userprofile__isnull=True)
        
        for user in users_without_profiles:
            UserProfile.objects.create(
                user=user,
                user_type='student'  # Default to student
            )
            self.stdout.write(
                self.style.SUCCESS(f'Created profile for user: {user.username}')
            )
        
        self.stdout.write(
            self.style.SUCCESS('All users now have profiles!')
        )