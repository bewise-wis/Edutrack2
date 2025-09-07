from django.db import models

class Result(models.Model):
    GRADE_CHOICES = (
        ('A', 'A (80-100)'),
        ('B', 'B (70-79)'),
        ('C', 'C (60-69)'),
        ('D', 'D (50-59)'),
        ('F', 'F (0-49)'),
    )
    
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    subject = models.ForeignKey('subjects.Subject', on_delete=models.CASCADE)
    term = models.CharField(max_length=20)
    academic_year = models.CharField(max_length=9)
    test_score = models.DecimalField(max_digits=5, decimal_places=2)
    exam_score = models.DecimalField(max_digits=5, decimal_places=2)
    total_score = models.DecimalField(max_digits=5, decimal_places=2)
    grade = models.CharField(max_length=1, choices=GRADE_CHOICES)
    teacher_comment = models.TextField(blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('student', 'subject', 'term', 'academic_year')
    
    def __str__(self):
        return f"{self.student} - {self.subject} - {self.term} {self.academic_year}"