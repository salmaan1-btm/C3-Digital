from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

def default_product_image():
    return 'static/images/stock.jpg'
# Create your models here.

class Dealership(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to = 'products/', blank = True)
    reorder_threshold = models.PositiveIntegerField(default=5)

    def __str__(self):
        return self.name

class Inventory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    dealership = models.ForeignKey(Dealership, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('product', 'dealership') # Ensures each dealership has a unique stock entry per product.
    def __str__(self):
        return f"{self.dealership.name} - {self.product.name} ({self.quantity} in stock)"

class Sale(models.Model):
    # A sales entry

    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    dealership = models.ForeignKey(Dealership, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    description = models.TextField(blank=True, null=True) 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateField(auto_now_add=True)
    
    def clean(self):
        """Ensure enough stock is available before completing a sale."""
        if self.inventory.quantity < self.quantity:
            raise ValidationError("Not enough stock available for this sale.")
        """Ensure product is from the right dealership"""
        if self.dealership != self.inventory.dealership:
            raise ValidationError("Dealership does not match Inventory.") 
        """Ensure sale quantity is greater than zero"""
        if self.quantity <=0:
            raise ValidationError("Quantity must be greater than 0.")
    def save(self, *args, **kwargs):
        self.clean()
        if self.inventory.quantity < self.quantity:
            raise ValidationError("Not enough stock available.")
        self.inventory.quantity -= self.quantity
        self.inventory.save()
        super().save(*args, **kwargs)
    def __str__(self):
        # Return a string representation of the model
        return f" {self.inventory.dealership.name} - {self.inventory.product.name} - {self.quantity} units"
    
class Claim(models.Model):
    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('initiated', 'Initiated'),
        ('rejected', 'Rejected'),
    ]

    name = models.CharField(max_length=255)  
    description = models.TextField(blank=True, null=True)
    dealership = models.ForeignKey(Dealership, on_delete=models.CASCADE)  
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='submitted')  
    created_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f"{self.name} - {self.get_status_display()}"

class Support(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()

    def __str__(self):
        return self.subject 
