# reports/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('reports/', views.report_list, name='report_list'),
    path('reports/student/generate/', views.generate_student_report, name='generate_student_report'),
    path('reports/class/generate/', views.generate_class_report, name='generate_class_report'),
    path('reports/<int:report_id>/view/', views.view_report, name='view_report'),
    path('reports/<int:report_id>/delete/', views.delete_report, name='delete_report'),
]