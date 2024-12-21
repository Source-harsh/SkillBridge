# mentor_matching/forms.py

from django import forms
from .models import Mentor

class MentorSearchForm(forms.Form):
    expertise = forms.CharField(required=False)
    availability = forms.CharField(required=False)
    teaching_mode = forms.ChoiceField(choices=[('hands-on', 'Hands-On'), ('virtual', 'Virtual')], required=False)
