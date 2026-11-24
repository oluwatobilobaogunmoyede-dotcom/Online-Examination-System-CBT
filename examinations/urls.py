from django.urls import path
from . import views

urlpatterns = [
    path('', views.examination_list, name='examination_list'),
    path('add/', views.examination_create, name='examination_create'),
    path('edit/<int:pk>/', views.examination_edit, name='examination_edit'),
    path('delete/<int:pk>/', views.examination_delete, name='examination_delete'),
]
