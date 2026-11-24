
from django.db import models
from academics.models import SchoolClass, Subject
from teachers.models import Teacher


class Examination(models.Model):
    title = models.CharField(max_length=200)

    school_class = models.ForeignKey(
        SchoolClass,
        on_delete=models.CASCADE,
        related_name='examinations'
    )

    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='examinations'
    )

    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='examinations'
    )

    instructions = models.TextField(blank=True)

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    duration = models.PositiveIntegerField(
        help_text="Duration in minutes"
    )

    total_marks = models.PositiveIntegerField(default=100)

    is_published = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
