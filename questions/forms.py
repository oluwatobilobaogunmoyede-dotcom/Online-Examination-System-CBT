
from django import forms
from .models import Question


class QuestionForm(forms.ModelForm):

    class Meta:
        model = Question

        fields = [
            'examination',
            'question_text',
            'option_a',
            'option_b',
            'option_c',
            'option_d',
            'correct_option',
            'marks',
        ]

        widgets = {
            'question_text': forms.Textarea(
                attrs={'rows': 4}
            ),
        }

    def clean_marks(self):
        marks = self.cleaned_data['marks']

        if marks <= 0:
            raise forms.ValidationError(
                "Marks must be greater than zero."
            )

        return marks
