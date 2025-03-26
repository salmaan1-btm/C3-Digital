from django.contrib import admin
from .models import Product
from .models import Claim
from .models import Sale

# Register your models here.

admin.site.register(Product)
admin.site.register(Claim)
admin.site.register(Sale)