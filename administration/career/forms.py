from django import forms
from riasec.models import Question, OfferedProgram
from accounts.models import Program


class AddCareerQuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ("question", "category")

        category_choices = [
            ("R", "Realistic"),
            ("I", "Investigative"),
            ("A", "Artistic"),
            ("S", "Social"),
            ("E", "Enterprising"),
            ("C", "Conventional"),
        ]

        widgets = {
            "question": forms.TextInput(attrs={"class": "form-control"}),
            "category": forms.Select(
                attrs={"class": "form-select"}, choices=category_choices
            ),
        }


class AddOfferedProgramForm(forms.ModelForm):
    program = forms.ModelChoiceField(
        widget=forms.Select(attrs={"class": "form-select"}),
        queryset=Program.objects.filter(department__educationlevel__name="College")
    )

    class Meta:
        model = OfferedProgram
        fields = ("interest", "program")

        widgets = {
            "interest": forms.Select(attrs={"class": "form-select"}),
        }
