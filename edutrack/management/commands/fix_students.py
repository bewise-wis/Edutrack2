from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from students.models import Student

class Command(BaseCommand):
    help = 'Fixes students without user accounts'

    def handle(self, *args, **options):
        students_without_users = Student.objects.filter(user__isnull=True)
        
        for student in students_without_users:
            # Create a user for this student
            username = f'student_{student.student_id}'
            email = f'{username}@example.com'
            
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    'first_name': 'Unknown',
                    'last_name': 'Student',
                    'password': 'temp123'  # Default password
                }
            )
            
            if created:
                student.user = user
                student.save()
                self.stdout.write(
                    self.style.SUCCESS(f'Created user for student: {student.student_id}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'User already exists for student: {student.student_id}')
                )
        
        self.stdout.write(
            self.style.SUCCESS('All students now have user accounts!')
        )