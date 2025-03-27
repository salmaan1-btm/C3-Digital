#C3_app1/sales_form.py

from django import forms
from .models import Sale, Product, User

class SalesForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['product_sold', 'quantity', 'description', 'dealership', 'user', 'status']
        labels = {
            'product_sold': 'Enter product',
            'quantity': 'Enter quantity',
            'description': 'Enter description (optional)',
            'user': 'Enter user',
            'status': 'Select status'
            }

