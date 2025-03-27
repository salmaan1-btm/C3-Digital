from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Dealership(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    stock = models.PositiveIntegerField(default=0)
    dealership = models.ForeignKey(Dealership, on_delete=models.CASCADE, null = True, blank = True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Sale(models.Model):
    # A sales entry
    name = models.CharField(max_length=200)
    product = models.TextField(blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True) 
    user = models.ForeignKey(User, on_delete=models.CASCADE, null = True, blank = True)

    def __str__(self):
        # Return a string representation of the model
        return self.name
    
class Claim(models.Model):
    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('initiated', 'Initiated'),
        ('rejected', 'Rejected'),
    ]

    name = models.CharField(max_length=255)  
    description = models.TextField(blank=True, null=True)  
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='submitted')  
    created_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f"{self.name} - {self.get_status_display()}"