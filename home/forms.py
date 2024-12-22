# forms.py

from django import forms
class SkillSearchForm(forms.Form):
    skill_name = forms.CharField(max_length=100, required=True, label="Enter Skill")
        
