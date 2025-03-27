#C3_app1/product_form.py

from django import forms
from .models import Sale, Product, User

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price']
        labels = {
            'name': 'Enter product name',
            'description': 'Enter description',
            'price': 'Enter price',
            }

