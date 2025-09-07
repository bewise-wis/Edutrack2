# reports/models.py
from django.db import models
from students.models import Student
from classes.models import Class
from subjects.models import Subject
from results.models import Result

class Report(models.Model):
    REPORT_TYPES = [
        ('student', 'Student Report'),
        ('class', 'Class Report'),
        ('performance', 'Performance Report'),
    ]
    
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
    title = models.CharField(max_length=200)
    generated_by = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    generated_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='reports/', null=True, blank=True)
    parameters = models.JSONField(default=dict)  # Stores report filters/parameters

    def __str__(self):
        return f"{self.title} - {self.generated_at}"

class StudentReport(models.Model):
    report = models.OneToOneField(Report, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    overall_average = models.DecimalField(max_digits=5, decimal_places=2)
    total_subjects = models.IntegerField()
    rank_in_class = models.IntegerField(null=True, blank=True)

class ClassReport(models.Model):
    report = models.OneToOneField(Report, on_delete=models.CASCADE)
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE)
    class_average = models.DecimalField(max_digits=5, decimal_places=2)
    total_students = models.IntegerField()
    pass_rate = models.DecimalField(max_digits=5, decimal_places=2)