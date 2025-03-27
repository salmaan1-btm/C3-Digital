#C3_app1/sales_form.py

from django import forms
from .models import Sale

class SalesForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['quantity']
        labels = {
            'quantity': 'Enter quantity',
            #'product': 'Enter product'
            }

