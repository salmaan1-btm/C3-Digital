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
            'name': 'Claim name',
            'description': 'Description',
            'user': 'Enter user',
            'status': 'Select claim status',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter claim name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter description'}),
            'user': forms.Select(attrs={'class': 'form-control'}),  
            'status': forms.Select(choices=Claim.STATUS_CHOICES)  # Dropdown for status
        }

class SupportForm(forms.Form):
    name = forms.CharField(label="Your Name", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="Your Email", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    subject = forms.CharField(label="Subject", max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))
    message = forms.CharField(label="Message", widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))
