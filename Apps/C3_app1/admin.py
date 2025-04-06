from django.contrib import admin
from .models import Product, Claim, Sale, Dealership, Inventory

# Register your models here.

admin.site.register(Product)
admin.site.register(Claim)
admin.site.register(Sale)

admin.site.register(Dealership)
admin.site.register(Inventory)
