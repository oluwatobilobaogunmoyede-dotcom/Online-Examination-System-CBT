from django.db import models
from django.conf import settings
from examinations.models import Examination


class ExamAttempt(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='exam_attempts'
    )

    examination = models.ForeignKey(
        Examination,
        on_delete=models.CASCADE,
        related_name='attempts'
    )

    started_at = models.DateTimeField(auto_now_add=True)

    submitted_at = models.DateTimeField(null=True, blank=True)

    score = models.PositiveIntegerField(default=0)

    is_submitted = models.BooleanField(default=False)

    class Meta:
        unique_together = ('student', 'examination')
        ordering = ['-started_at']

    def __str__(self):
        return f"{self.student.username} - {self.examination.title}"


class StudentAnswer(models.Model):
    OPTION_CHOICES = [
        ('A', 'Option A'),
        ('B', 'Option B'),
        ('C', 'Option C'),
        ('D', 'Option D'),
    ]

    attempt = models.ForeignKey(
        ExamAttempt,
        on_delete=models.CASCADE,
        related_name='answers'
    )

    question = models.ForeignKey(
        'questions.Question',
        on_delete=models.CASCADE,
        related_name='student_answers'
    )

    selected_option = models.CharField(
        max_length=1,
        choices=OPTION_CHOICES,
        blank=True
    )

    is_correct = models.BooleanField(default=False)

    marks_awarded = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('attempt', 'question')

    def __str__(self):
        return f"{self.attempt.student.username} - Question {self.question.id}"

