
from django import forms
from .models import SchoolClass, Subject


class SchoolClassForm(forms.ModelForm):
    class Meta:
        model = SchoolClass
        fields = ['name', 'description']


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = [
            'name',
            'code',
            'school_class',
            'teacher',
            'description',
        ]
