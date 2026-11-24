from django.contrib import admin
from .models import ExamAttempt, StudentAnswer


@admin.register(ExamAttempt)
class ExamAttemptAdmin(admin.ModelAdmin):
    list_display = (
        'student',
        'examination',
        'score',
        'started_at',
        'submitted_at',
        'is_submitted',
    )

    list_filter = ('is_submitted', 'examination')

    search_fields = (
        'student__username',
        'examination__title',
    )


@admin.register(StudentAnswer)
class StudentAnswerAdmin(admin.ModelAdmin):
    list_display = (
        'attempt',
        'question',
        'selected_option',
        'is_correct',
        'marks_awarded',
    )

    list_filter = ('selected_option', 'is_correct')
