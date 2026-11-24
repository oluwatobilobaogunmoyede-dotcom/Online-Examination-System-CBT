
from django.contrib import admin
from .models import Question


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = (
        'question_text',
        'examination',
        'correct_option',
        'marks',
        'created_at',
    )

    list_filter = ('examination', 'correct_option')

    search_fields = ('question_text',)
