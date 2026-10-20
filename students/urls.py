
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add/', views.add_student, name='add_student'),
    path('edit/<int:id>/', views.edit_student, name='edit_student'),
    path('view/<int:id>/', views.view_student, name='view_student'),
    path('manage-students/delete/', views.delete_student_page, name='delete_student_page'),
    path('manage-students/delete/<int:id>/', views.delete_student, name='delete_student'),
]
