from django import forms
from django.contrib.auth.models import User
from .models import Student

class StudentForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=False)
    
    class Meta:
        model = Student
        exclude = ['user']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Only populate fields if we're editing an existing student with a user
        if self.instance and self.instance.pk and hasattr(self.instance, 'user') and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email
        else:
            # Set default values for new students
            self.fields['password'].required = True
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        # Check if email is already used by another user
        if self.instance and self.instance.pk and hasattr(self.instance, 'user') and self.instance.user:
            # Editing existing student - exclude current user
            if User.objects.filter(email=email).exclude(id=self.instance.user.id).exists():
                raise forms.ValidationError('This email is already in use.')
        else:
            # Creating new student
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError('This email is already in use.')
        
        return email
    
    def save(self, commit=True):
        student = super().save(commit=False)
        
        if student.pk and hasattr(student, 'user') and student.user:
            # Update existing user
            user = student.user
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.email = self.cleaned_data['email']
            
            if self.cleaned_data['password']:
                user.set_password(self.cleaned_data['password'])
            
            user.save()
        else:
            # Create new user
            user = User.objects.create_user(
                username=self.cleaned_data['email'],
                email=self.cleaned_data['email'],
                password=self.cleaned_data['password'],
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name']
            )
            student.user = user
        
        if commit:
            student.save()
        
        return student