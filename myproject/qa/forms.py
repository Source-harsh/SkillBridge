# qa/forms.py
from django import forms
from .models import Question, Reply

# Form to submit a question
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'content']

# Form to reply to a question
class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['content']
