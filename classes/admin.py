from django.contrib import admin
from .models import Class

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'capacity', 'class_teacher')
    list_filter = ('capacity',)
    search_fields = ('name', 'code')