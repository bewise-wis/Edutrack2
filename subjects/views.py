from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Subject
from .forms import SubjectForm

@login_required
def subject_list(request):
    if request.user.userprofile.user_type != 'admin':
        messages.error(request, 'You do not have permission to view this page.')
        return redirect('dashboard')
    
    subjects = Subject.objects.all()
    return render(request, 'subjects/subject_list.html', {'subjects': subjects})

@login_required
def subject_create(request):
    if request.user.userprofile.user_type != 'admin':
        messages.error(request, 'You do not have permission to perform this action.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            subject = form.save()
            messages.success(request, f'Subject {subject.name} created successfully.')
            return redirect('subject_list')
    else:
        form = SubjectForm()
    
    return render(request, 'subjects/subject_form.html', {'form': form, 'title': 'Add New Subject'})

@login_required
def subject_update(request, pk):
    if request.user.userprofile.user_type != 'admin':
        messages.error(request, 'You do not have permission to perform this action.')
        return redirect('dashboard')
    
    subject = get_object_or_404(Subject, pk=pk)
    
    if request.method == 'POST':
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            messages.success(request, f'Subject {subject.name} updated successfully.')
            return redirect('subject_list')
    else:
        form = SubjectForm(instance=subject)
    
    return render(request, 'subjects/subject_form.html', {'form': form, 'title': 'Edit Subject'})

@login_required
def subject_delete(request, pk):
    if request.user.userprofile.user_type != 'admin':
        messages.error(request, 'You do not have permission to perform this action.')
        return redirect('dashboard')
    
    subject = get_object_or_404(Subject, pk=pk)
    
    if request.method == 'POST':
        subject_name = subject.name
        subject.delete()
        messages.success(request, f'Subject {subject_name} deleted successfully.')
        return redirect('subject_list')
    
    return render(request, 'subjects/subject_confirm_delete.html', {'subject': subject})