# queryapp/forms.py
from django import forms

class QueryForm(forms.Form):
    query = forms.CharField(label='Search for a product', max_length=100)
