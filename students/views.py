from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Student
from .forms import StudentForm

@login_required
def student_list(request):
    if request.user.userprofile.user_type not in ['admin', 'teacher']:
        messages.error(request, 'You do not have permission to view this page.')
        return redirect('dashboard')
    
    students = Student.objects.select_related('user', 'current_class').all()
    
    # Check for students without users and fix them
    for student in students:
        if not hasattr(student, 'user') or not student.user:
            # Create a user for this student
            user = User.objects.create_user(
                username=f'student_{student.student_id}',
                email=f'student_{student.student_id}@example.com',
                password='temp123',
                first_name='Unknown',
                last_name='Student'
            )
            student.user = user
            student.save()
    
    return render(request, 'students/student_list.html', {'students': students})

@login_required
def student_detail(request, pk):
    if request.user.userprofile.user_type not in ['admin', 'teacher']:
        messages.error(request, 'You do not have permission to view this page.')
        return redirect('dashboard')
    
    student = get_object_or_404(Student, pk=pk)
    
    # Ensure student has a user
    if not hasattr(student, 'user') or not student.user:
        # Create a default user for this student
        user = User.objects.create_user(
            username=f'student_{student.student_id}',
            email=f'student_{student.student_id}@example.com',
            password='temp123',
            first_name='Unknown',
            last_name='Student'
        )
        student.user = user
        student.save()
        messages.info(request, 'A user account was created for this student.')
    
    return render(request, 'students/student_detail.html', {'student': student})

@login_required
def student_create(request):
    if request.user.userprofile.user_type != 'admin':
        messages.error(request, 'You do not have permission to perform this action.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            try:
                student = form.save()
                messages.success(request, f'Student {student.user.get_full_name()} created successfully.')
                return redirect('student_list')
            except Exception as e:
                messages.error(request, f'Error creating student: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = StudentForm()
    
    return render(request, 'students/student_form.html', {'form': form, 'title': 'Add New Student'})

@login_required
def student_update(request, pk):
    if request.user.userprofile.user_type != 'admin':
        messages.error(request, 'You do not have permission to perform this action.')
        return redirect('dashboard')
    
    student = get_object_or_404(Student, pk=pk)
    
    # Check if student has a user, if not create one
    if not hasattr(student, 'user') or not student.user:
        # Create a default user for this student
        user = User.objects.create_user(
            username=f'student_{student.student_id}',
            email=f'student_{student.student_id}@example.com',
            password='temp123',
            first_name='Unknown',
            last_name='Student'
        )
        student.user = user
        student.save()
        messages.info(request, 'A user account was created for this student.')
    
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, f'Student {student.user.get_full_name()} updated successfully.')
                return redirect('student_list')
            except Exception as e:
                messages.error(request, f'Error updating student: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = StudentForm(instance=student)
    
    return render(request, 'students/student_form.html', {'form': form, 'title': 'Edit Student'})

@login_required
def student_delete(request, pk):
    if request.user.userprofile.user_type != 'admin':
        messages.error(request, 'You do not have permission to perform this action.')
        return redirect('dashboard')
    
    student = get_object_or_404(Student, pk=pk)
    
    if request.method == 'POST':
        student_name = student.user.get_full_name() if hasattr(student, 'user') and student.user else student.student_id
        # Delete the associated user if it exists
        if hasattr(student, 'user') and student.user:
            student.user.delete()
        student.delete()
        messages.success(request, f'Student {student_name} deleted successfully.')
        return redirect('student_list')
    
    student_name = student.user.get_full_name() if hasattr(student, 'user') and student.user else student.student_id
    return render(request, 'students/student_confirm_delete.html', {'student': student, 'student_name': student_name})