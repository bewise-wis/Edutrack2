from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student')
    student_id = models.CharField(max_length=20, unique=True)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    parent_name = models.CharField(max_length=100)
    parent_phone = models.CharField(max_length=15)
    address = models.TextField()
    enrollment_date = models.DateField(auto_now_add=True)
    current_class = models.ForeignKey('classes.Class', on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        if hasattr(self, 'user') and self.user:
            return f"{self.user.get_full_name()} ({self.student_id})"
        return f"Unknown Student ({self.student_id})"
    
    def save(self, *args, **kwargs):
        # Ensure student has a user account
        if not hasattr(self, 'user') or not self.user:
            # Create a default user
            from django.contrib.auth.models import User
            user = User.objects.create_user(
                username=f'student_{self.student_id}',
                email=f'student_{self.student_id}@example.com',
                password='temp123',
                first_name='Unknown',
                last_name='Student'
            )
            self.user = user
        super().save(*args, **kwargs)