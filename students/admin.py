from django.contrib import admin
from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('admission_number', 'user', 'gender', 'created_at')
    search_fields = ('admission_number', 'user__username', 'user__first_name', 'user__last_name')
    list_filter = ('gender',)
