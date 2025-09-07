from django.contrib import admin
from .models import Result

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'term', 'academic_year', 'total_score', 'grade')
    list_filter = ('term', 'academic_year', 'grade')
    search_fields = ('student__user__first_name', 'student__user__last_name', 'subject__name')