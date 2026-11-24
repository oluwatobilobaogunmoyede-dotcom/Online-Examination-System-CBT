
from django import forms
from django.contrib.auth import get_user_model
from .models import Teacher

User = get_user_model()


class TeacherForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(
        widget=forms.PasswordInput
    )

    class Meta:
        model = Teacher
        fields = [
            'employee_number',
            'qualification',
            'specialization',
            'phone',
            'address',
        ]

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists.")
        return username

    def clean_employee_number(self):
        number = self.cleaned_data['employee_number']
        if Teacher.objects.filter(employee_number=number).exists():
            raise forms.ValidationError("Employee number already exists.")
        return number
