
from django.db import models
from teachers.models import Teacher


class SchoolClass(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subjects'
    )
    school_class = models.ForeignKey(
        SchoolClass,
        on_delete=models.CASCADE,
        related_name='subjects'
    )
    description = models.TextField(blank=True)

    class Meta:
        unique_together = ('name', 'school_class')

    def __str__(self):
        return f"{self.name} - {self.school_class.name}"
