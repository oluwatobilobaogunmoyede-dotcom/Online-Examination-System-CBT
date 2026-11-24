
from django.contrib import admin
from .models import SchoolClass, Subject


@admin.register(SchoolClass)
class SchoolClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'school_class', 'teacher')
    list_filter = ('school_class',)
    search_fields = ('name', 'code')
