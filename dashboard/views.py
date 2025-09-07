from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from students.models import Student
from teachers.models import Teacher
from classes.models import Class
from results.models import Result

@login_required
def dashboard(request):
    # Get counts for dashboard
    student_count = Student.objects.count()
    teacher_count = Teacher.objects.count()
    class_count = Class.objects.count()
    result_count = Result.objects.count()
    
    # Get recent results
    recent_results = Result.objects.select_related('student__user', 'subject')[:5]
    
    context = {
        'student_count': student_count,
        'teacher_count': teacher_count,
        'class_count': class_count,
        'result_count': result_count,
        'recent_results': recent_results,
    }
    
    return render(request, 'dashboard/dashboard.html', context)