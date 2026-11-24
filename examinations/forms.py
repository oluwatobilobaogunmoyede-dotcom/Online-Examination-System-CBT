
from django import forms
from .models import Examination


class ExaminationForm(forms.ModelForm):
    class Meta:
        model = Examination
        fields = [
            'title',
            'school_class',
            'subject',
            'teacher',
            'instructions',
            'start_time',
            'end_time',
            'duration',
            'total_marks',
            'is_published',
        ]

        widgets = {
            'instructions': forms.Textarea(attrs={
                'rows': 4
            }),
            'start_time': forms.DateTimeInput(attrs={
                'type': 'datetime-local'
            }),
            'end_time': forms.DateTimeInput(attrs={
                'type': 'datetime-local'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()

        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        duration = cleaned_data.get('duration')
        subject = cleaned_data.get('subject')
        school_class = cleaned_data.get('school_class')

        if start_time and end_time and end_time <= start_time:
            self.add_error(
                'end_time',
                'End time must be after start time.'
            )

        if duration is not None and duration <= 0:
            self.add_error(
                'duration',
                'Duration must be greater than zero.'
            )

        if subject and school_class:
            if subject.school_class_id != school_class.id:
                self.add_error(
                    'subject',
                    'This subject does not belong to the selected class.'
                )

        return cleaned_data
