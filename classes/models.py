from django.db import models

class Class(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=10, unique=True)
    capacity = models.PositiveIntegerField()
    class_teacher = models.ForeignKey('teachers.Teacher', on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return self.name