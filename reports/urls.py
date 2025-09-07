from django.urls import path
from . import views

urlpatterns = [
    path('', views.report_list, name='report_list'),
    path('student/<int:student_id>/', views.student_report, name='student_report'),
    path('class/<int:class_id>/', views.class_report, name='class_report'),
]