from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'user', 'current_class', 'gender', 'date_of_birth')
    list_filter = ('current_class', 'gender')
    search_fields = ('student_id', 'user__first_name', 'user__last_name')