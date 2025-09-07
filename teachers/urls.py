from django.urls import path
from . import views

urlpatterns = [
    path('', views.teacher_list, name='teacher_list'),
    path('create/', views.teacher_create, name='teacher_create'),
    path('<int:pk>/', views.teacher_detail, name='teacher_detail'),
    path('<int:pk>/update/', views.teacher_update, name='teacher_update'),
    path('<int:pk>/delete/', views.teacher_delete, name='teacher_delete'),
]