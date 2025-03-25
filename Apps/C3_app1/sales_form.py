#C3_app1/sales_form.py

from django import forms
from .models import Sales

class SalesForm(forms.ModelForm):
    class Meta:
        model = Sales
        fields = ['text']
        labels = {'text': 'Enter text'}

