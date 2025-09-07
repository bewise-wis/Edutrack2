from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Class
from .forms import ClassForm

@login_required
def class_list(request):
    if request.user.userprofile.user_type != 'admin':
        messages.error(request, 'You do not have permission to view this page.')
        return redirect('dashboard')
    
    classes = Class.objects.select_related('class_teacher__user').all()
    return render(request, 'classes/class_list.html', {'classes': classes})

@login_required
def class_create(request):
    if request.user.userprofile.user_type != 'admin':
        messages.error(request, 'You do not have permission to perform this action.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = ClassForm(request.POST)
        if form.is_valid():
            class_obj = form.save()
            messages.success(request, f'Class {class_obj.name} created successfully.')
            return redirect('class_list')
    else:
        form = ClassForm()
    
    return render(request, 'classes/class_form.html', {'form': form, 'title': 'Add New Class'})

@login_required
def class_update(request, pk):
    if request.user.userprofile.user_type != 'admin':
        messages.error(request, 'You do not have permission to perform this action.')
        return redirect('dashboard')
    
    class_obj = get_object_or_404(Class, pk=pk)
    
    if request.method == 'POST':
        form = ClassForm(request.POST, instance=class_obj)
        if form.is_valid():
            form.save()
            messages.success(request, f'Class {class_obj.name} updated successfully.')
            return redirect('class_list')
    else:
        form = ClassForm(instance=class_obj)
    
    return render(request, 'classes/class_form.html', {'form': form, 'title': 'Edit Class'})

@login_required
def class_delete(request, pk):
    if request.user.userprofile.user_type != 'admin':
        messages.error(request, 'You do not have permission to perform this action.')
        return redirect('dashboard')
    
    class_obj = get_object_or_404(Class, pk=pk)
    
    if request.method == 'POST':
        class_name = class_obj.name
        class_obj.delete()
        messages.success(request, f'Class {class_name} deleted successfully.')
        return redirect('class_list')
    
    return render(request, 'classes/class_confirm_delete.html', {'class_obj': class_obj})