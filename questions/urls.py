from django.urls import path
from . import views

urlpatterns = [
    path('', views.question_list, name='question_list'),
    path('add/', views.question_create, name='question_create'),
    path('edit/<int:pk>/', views.question_edit, name='question_edit'),
    path('delete/<int:pk>/', views.question_delete, name='question_delete'),
]
