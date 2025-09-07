from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from students.models import Student
from results.models import Result

@login_required
def report_list(request):
    if request.user.userprofile.user_type != 'admin':
        messages.error(request, 'You do not have permission to view this page.')
        return redirect('dashboard')
    
    # You can add report generation logic here
    return render(request, 'reports/report_list.html')

@login_required
def student_report(request, student_id):
    if request.user.userprofile.user_type != 'admin':
        messages.error(request, 'You do not have permission to view this page.')
        return redirect('dashboard')
    
    student = Student.objects.get(pk=student_id)
    results = Result.objects.filter(student=student).select_related('subject')
    
    context = {
        'student': student,
        'results': results
    }
    
    return render(request, 'reports/student_report.html', context)

@login_required
def class_report(request, class_id):
    if request.user.userprofile.user_type != 'admin':
        messages.error(request, 'You do not have permission to view this page.')
        return redirect('dashboard')
    
    # You can add class report logic here
    return render(request, 'reports/class_report.html')