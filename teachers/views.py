from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Teacher
from .forms import TeacherForm

@login_required
def teacher_list(request):
    if request.user.userprofile.user_type != 'admin':
        messages.error(request, 'You do not have permission to view this page.')
        return redirect('dashboard')
    
    teachers = Teacher.objects.select_related('user').all()
    return render(request, 'teachers/teacher_list.html', {'teachers': teachers})

@login_required
def teacher_detail(request, pk):
    if request.user.userprofile.user_type != 'admin':
        messages.error(request, 'You do not have permission to view this page.')
        return redirect('dashboard')
    
    teacher = get_object_or_404(Teacher, pk=pk)
    return render(request, 'teachers/teacher_detail.html', {'teacher': teacher})

@login_required
def teacher_create(request):
    if request.user.userprofile.user_type != 'admin':
        messages.error(request, 'You do not have permission to perform this action.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            teacher = form.save()
            messages.success(request, f'Teacher {teacher.user.get_full_name()} created successfully.')
            return redirect('teacher_list')
    else:
        form = TeacherForm()
    
    return render(request, 'teachers/teacher_form.html', {'form': form, 'title': 'Add New Teacher'})

@login_required
def teacher_update(request, pk):
    if request.user.userprofile.user_type != 'admin':
        messages.error(request, 'You do not have permission to perform this action.')
        return redirect('dashboard')
    
    teacher = get_object_or_404(Teacher, pk=pk)
    
    if request.method == 'POST':
        form = TeacherForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save()
            messages.success(request, f'Teacher {teacher.user.get_full_name()} updated successfully.')
            return redirect('teacher_list')
    else:
        form = TeacherForm(instance=teacher)
    
    return render(request, 'teachers/teacher_form.html', {'form': form, 'title': 'Edit Teacher'})

@login_required
def teacher_delete(request, pk):
    if request.user.userprofile.user_type != 'admin':
        messages.error(request, 'You do not have permission to perform this action.')
        return redirect('dashboard')
    
    teacher = get_object_or_404(Teacher, pk=pk)
    
    if request.method == 'POST':
        teacher_name = teacher.user.get_full_name()
        teacher.delete()
        messages.success(request, f'Teacher {teacher_name} deleted successfully.')
        return redirect('teacher_list')
    
    return render(request, 'teachers/teacher_confirm_delete.html', {'teacher': teacher})