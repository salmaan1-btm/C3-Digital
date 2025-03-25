from django.contrib import admin
from .models import Product
from .models import Claim

# Register your models here.

admin.site.register(Product)
admin.site.register(Claim)