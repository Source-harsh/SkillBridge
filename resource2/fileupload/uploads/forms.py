from django import forms
from .models import SubjectFile

class SubjectFileForm(forms.ModelForm):
    class Meta:
        model = SubjectFile
        fields = ['subject', 'file']