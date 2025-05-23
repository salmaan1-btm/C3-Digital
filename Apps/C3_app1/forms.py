from django import forms
from .models import Sale, Product, User, Claim, Inventory, Support, Dealership

class SalesForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['inventory', 'dealership','quantity', 'description', 'user']
        labels = {
            'inventory': 'Select product from inventory',
            'dealership': 'Select dealership',
            'quantity': 'Enter quantity',
            'description': 'Enter description (optional)',
            'user': 'Enter user',
            }
        widgets = {
            'inventory': forms.Select(attrs={'class': 'form-control'}),
            'dealership': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter quantity'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter description (optional)'}),
            'user': forms.Select(attrs={'class': 'form-control'}), 
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image']
        labels = {
            'name': 'Enter product name',
            'description': 'Enter description',
            'price': 'Enter price',
            'image': 'Upload product image',
            }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter product name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter description'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter price'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class InventoryForm(forms.Form):
    product = forms.ModelChoiceField(queryset=Product.objects.all(), widget=forms.Select(attrs={'class':'form-control'}))
    dealership = forms.ModelChoiceField(queryset=Dealership.objects.all(), widget=forms.Select(attrs={'class':'form-control'}))
    quantity = forms.IntegerField(min_value=1, widget=forms.NumberInput(attrs={'class':'form-control'}))

class ClaimsForm(forms.ModelForm):
    class Meta:
        model = Claim
        fields = ['name', 'description', 'dealership', 'user', 'status']
        labels = {
            'name': 'Claim name',
            'description': 'Description',
            'dealership': 'Select dealership',
            'user': 'Enter user',
            'status': 'Select claim status',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter claim name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter description'}),
            'dealership': forms.Select(attrs={'class': 'form-control'}),
            'user': forms.Select(attrs={'class': 'form-control'}),  
            'status': forms.Select(choices=Claim.STATUS_CHOICES)
        }

class SupportForm(forms.ModelForm):
    class Meta:
        model = Support
        fields = ['name', 'email', 'subject', 'message']
        labels = {
            'name': 'Your Name',
            'email': 'Your Email',
            'subject': 'Subject',
            'message': 'Message',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'class': 'form-control'}),  
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5})
        }