
from django.contrib import admin
from .models import Teacher


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = (
        'employee_number',
        'user',
        'qualification',
        'specialization',
    )
    search_fields = (
        'employee_number',
        'user__username',
        'user__first_name',
        'user__last_name',
    )
