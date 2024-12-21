# forms.py

from django import forms
from .models import CollaborationRequest


class CollaborationRequestForm(forms.ModelForm):
    class Meta:
        model = CollaborationRequest
        fields = ['skill_needed', 'professionalism_level_needed']
        widgets = {
            'skill_needed': forms.TextInput(attrs={'placeholder': 'Enter skill needed'}),
            'professionalism_level_needed': forms.Select(choices=CollaborationRequest._meta.get_field('professionalism_level_needed').choices)
        }
