from django import forms
from .models import Sale, Product, User, Claim

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

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price']
        labels = {
            'name': 'Enter product name',
            'description': 'Enter description',
            'price': 'Enter price',
            }

class ClaimsForm(forms.ModelForm):
    class Meta:
        model = Claim
        fields = ['name', 'description', 'user', 'status']
        labels = {
            'name': 'Enter claim name',
            'description': 'Enter description',
            'user': 'Enter user',
            'status': 'Select claim status',
        }
        widgets = {
            'status': forms.Select(choices=Claim.STATUS_CHOICES)  # Dropdown for status
        }
