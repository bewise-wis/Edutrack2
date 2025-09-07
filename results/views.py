from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Result
from .forms import ResultForm
from students.models import Student

@login_required
def result_list(request):
    if request.user.userprofile.user_type not in ['admin', 'teacher']:
        messages.error(request, 'You do not have permission to view this page.')
        return redirect('dashboard')
    
    results = Result.objects.select_related('student__user', 'subject').all()
    return render(request, 'results/result_list.html', {'results': results})

@login_required
def result_create(request):
    if request.user.userprofile.user_type not in ['admin', 'teacher']:
        messages.error(request, 'You do not have permission to perform this action.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = ResultForm(request.POST)
        if form.is_valid():
            result = form.save()
            messages.success(request, f'Result for {result.student.user.get_full_name()} created successfully.')
            return redirect('result_list')
    else:
        form = ResultForm()
    
    return render(request, 'results/result_form.html', {'form': form, 'title': 'Add New Result'})

@login_required
def result_update(request, pk):
    if request.user.userprofile.user_type not in ['admin', 'teacher']:
        messages.error(request, 'You do not have permission to perform this action.')
        return redirect('dashboard')
    
    result = get_object_or_404(Result, pk=pk)
    
    if request.method == 'POST':
        form = ResultForm(request.POST, instance=result)
        if form.is_valid():
            form.save()
            messages.success(request, f'Result for {result.student.user.get_full_name()} updated successfully.')
            return redirect('result_list')
    else:
        form = ResultForm(instance=result)
    
    return render(request, 'results/result_form.html', {'form': form, 'title': 'Edit Result'})

@login_required
def result_delete(request, pk):
    if request.user.userprofile.user_type not in ['admin', 'teacher']:
        messages.error(request, 'You do not have permission to perform this action.')
        return redirect('dashboard')
    
    result = get_object_or_404(Result, pk=pk)
    
    if request.method == 'POST':
        student_name = result.student.user.get_full_name()
        result.delete()
        messages.success(request, f'Result for {student_name} deleted successfully.')
        return redirect('result_list')
    
    return render(request, 'results/result_confirm_delete.html', {'result': result})

@login_required
def my_results(request):
    if request.user.userprofile.user_type != 'student':
        messages.error(request, 'You do not have permission to view this page.')
        return redirect('dashboard')
    
    try:
        student = request.user.student
        results = Result.objects.filter(student=student).select_related('subject')
        
        # Calculate average and other statistics
        if results:
            total_score = sum([result.total_score for result in results])
            average_score = (total_score / len(results))
            
            # Determine grade based on average
            if average_score >= 80:
                average_grade = 'A'
            elif average_score >= 70:
                average_grade = 'B'
            elif average_score >= 60:
                average_grade = 'C'
            elif average_score >= 50:
                average_grade = 'D'
            else:
                average_grade = 'F'
        else:
            average_score = 0
            average_grade = 'N/A'
        
        context = {
            'results': results,
            'average_score': average_score,
            'average_grade': average_grade,
            'student': student
        }
        
        return render(request, 'results/my_results.html', context)
    
    except AttributeError:
        messages.error(request, 'Student profile not found.')
        return redirect('dashboard')