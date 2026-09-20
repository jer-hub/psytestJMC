from django import forms
from iqtest.models import Question, Choice
from django_quill.forms import QuillFormField
from django.utils.html import strip_tags
from iqtest.quill_images import compress_quill_json
import json

class AddIQQuestionForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['question'].error_messages = {'required': 'Please write a question'}

    question = QuillFormField()
    class Meta:
        model = Question
        fields = ("question",)

    def clean_question(self):
        json_question = json.loads(self.cleaned_data['question'])
        question_str = strip_tags(json_question['html'])
        if question_str == '' and 'data:image' not in json_question.get('html', '') and '<img' not in json_question.get('html', ''):
            self.add_error('question', 'Please write a question')
            return False
        return compress_quill_json(self.cleaned_data['question'])

class AddIQChoiceForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['question'].widget = forms.HiddenInput()

    choice = QuillFormField()
    class Meta:
        model = Choice
        fields = ('question', 'choice', 'is_answer')
        widgets = {
            'is_answer': forms.Select(choices=Choice.answerTextChoices.choices[1:],attrs={'class': 'form-select w-50'}),
        }

    def clean_choice(self):
        return compress_quill_json(self.cleaned_data['choice'])
