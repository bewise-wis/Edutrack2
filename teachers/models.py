from django.db import models
from django.contrib.auth.models import User

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    teacher_id = models.CharField(max_length=20, unique=True)
    date_of_birth = models.DateField()
    qualification = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    date_joined = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} ({self.teacher_id})"