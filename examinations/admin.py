
from django.contrib import admin
from .models import Examination


@admin.register(Examination)
class ExaminationAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'school_class',
        'subject',
        'teacher',
        'start_time',
        'end_time',
        'is_published',
    )

    list_filter = ('school_class', 'subject', 'is_published')

    search_fields = ('title', 'subject__name')
