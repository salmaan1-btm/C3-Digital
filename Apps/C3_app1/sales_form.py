#C3_app1/sales_form.py

from django import forms
from .models import Sale

class SalesForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['name', 'product']
        labels = {
            'name': 'Enter name',
            'product': 'Enter product'
            }

