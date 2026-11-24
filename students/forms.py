from django import forms
from django.contrib.auth import get_user_model
from .models import Student

User = get_user_model()


class StudentForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(
        widget=forms.PasswordInput
    )

    class Meta:
        model = Student
        fields = [
            'admission_number',
            'date_of_birth',
            'gender',
            'address',
        ]
        widgets = {
            'date_of_birth': forms.DateInput(
                attrs={'type': 'date'}
            ),
        }

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists.")
        return username

    def clean_admission_number(self):
        admission_number = self.cleaned_data['admission_number']
        if Student.objects.filter(admission_number=admission_number).exists():
            raise forms.ValidationError("Admission number already exists.")
        return admission_number
