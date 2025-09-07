from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import UserProfile
from students.models import Student
from teachers.models import Teacher
from classes.models import Class
from subjects.models import Subject
from results.models import Result
import datetime

class Command(BaseCommand):
    help = 'Sets up initial data for the application'

    def handle(self, *args, **options):
        self.stdout.write('Setting up initial data...')
        
        # Create admin user
        admin_user, created = User.objects.get_or_create(
            username='admin@edutrack.com',
            defaults={
                'email': 'admin@edutrack.com',
                'first_name': 'System',
                'last_name': 'Administrator',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS('Created admin user'))
        else:
            self.stdout.write(self.style.WARNING('Admin user already exists'))
        
        # Create admin profile
        admin_profile, created = UserProfile.objects.get_or_create(
            user=admin_user,
            defaults={'user_type': 'admin'}
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Created admin profile'))
        else:
            self.stdout.write(self.style.WARNING('Admin profile already exists'))
        
        # Create sample teacher
        teacher_user, created = User.objects.get_or_create(
            username='teacher@edutrack.com',
            defaults={
                'email': 'teacher@edutrack.com',
                'first_name': 'John',
                'last_name': 'Smith'
            }
        )
        if created:
            teacher_user.set_password('teacher123')
            teacher_user.save()
            self.stdout.write(self.style.SUCCESS('Created teacher user'))
        else:
            self.stdout.write(self.style.WARNING('Teacher user already exists'))
        
        teacher_profile, created = UserProfile.objects.get_or_create(
            user=teacher_user,
            defaults={'user_type': 'teacher'}
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Created teacher profile'))
        else:
            self.stdout.write(self.style.WARNING('Teacher profile already exists'))
        
        teacher, created = Teacher.objects.get_or_create(
            user=teacher_user,
            defaults={
                'teacher_id': 'T001',
                'date_of_birth': datetime.date(1980, 5, 15),
                'qualification': 'M.Ed in Mathematics',
                'specialization': 'Mathematics and Physics'
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Created teacher record'))
        else:
            self.stdout.write(self.style.WARNING('Teacher record already exists'))
        
        # Create sample class
        math_class, created = Class.objects.get_or_create(
            name='Form 4A',
            code='F4A',
            defaults={
                'capacity': 40,
                'class_teacher': teacher
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Created class'))
        else:
            self.stdout.write(self.style.WARNING('Class already exists'))
        
        # Create sample student
        student_user, created = User.objects.get_or_create(
            username='student@edutrack.com',
            defaults={
                'email': 'student@edutrack.com',
                'first_name': 'Jane',
                'last_name': 'Doe'
            }
        )
        if created:
            student_user.set_password('student123')
            student_user.save()
            self.stdout.write(self.style.SUCCESS('Created student user'))
        else:
            self.stdout.write(self.style.WARNING('Student user already exists'))
        
        student_profile, created = UserProfile.objects.get_or_create(
            user=student_user,
            defaults={'user_type': 'student'}
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Created student profile'))
        else:
            self.stdout.write(self.style.WARNING('Student profile already exists'))
        
        student, created = Student.objects.get_or_create(
            user=student_user,
            defaults={
                'student_id': 'S001',
                'date_of_birth': datetime.date(2007, 3, 10),
                'gender': 'F',
                'parent_name': 'John Doe Sr.',
                'parent_phone': '+1234567890',
                'address': '123 Main Street, City, State',
                'current_class': math_class
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Created student record'))
        else:
            self.stdout.write(self.style.WARNING('Student record already exists'))
        
        # Create sample subjects
        subjects_data = [
            {'name': 'Mathematics', 'code': 'MATH'},
            {'name': 'English', 'code': 'ENG'},
            {'name': 'Science', 'code': 'SCI'},
            {'name': 'History', 'code': 'HIST'},
            {'name': 'Geography', 'code': 'GEOG'},
        ]
        
        for subject_data in subjects_data:
            subject, created = Subject.objects.get_or_create(
                code=subject_data['code'],
                defaults=subject_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created subject: {subject_data["name"]}'))
            else:
                self.stdout.write(self.style.WARNING(f'Subject already exists: {subject_data["name"]}'))
        
        # Create sample results
        math_subject = Subject.objects.get(code='MATH')
        english_subject = Subject.objects.get(code='ENG')
        
        # Math result
        math_result, created = Result.objects.get_or_create(
            student=student,
            subject=math_subject,
            term='First Term',
            academic_year='2023-2024',
            defaults={
                'test_score': 25,
                'exam_score': 62,
                'total_score': 87,
                'grade': 'A',
                'teacher_comment': 'Excellent performance'
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Created math result'))
        else:
            self.stdout.write(self.style.WARNING('Math result already exists'))
        
        # English result
        english_result, created = Result.objects.get_or_create(
            student=student,
            subject=english_subject,
            term='First Term',
            academic_year='2023-2024',
            defaults={
                'test_score': 22,
                'exam_score': 58,
                'total_score': 80,
                'grade': 'A',
                'teacher_comment': 'Good writing skills'
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Created English result'))
        else:
            self.stdout.write(self.style.WARNING('English result already exists'))
        
        self.stdout.write(self.style.SUCCESS('Initial data setup completed successfully!'))
        self.stdout.write('')
        self.stdout.write('Login credentials:')
        self.stdout.write('Admin: admin@edutrack.com / admin123')
        self.stdout.write('Teacher: teacher@edutrack.com / teacher123')
        self.stdout.write('Student: student@edutrack.com / student123')