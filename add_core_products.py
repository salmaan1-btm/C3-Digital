import os
import django

# Set up Django settings before importing models
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "C3_Website.settings")

# Initialize Django
django.setup()

# Now import your models after setting up Django settings
from Apps.C3_app1.models import Product

def add_core_products():
    core_products = [
        {
            'name': 'Rust Protection',
            'description': 'Prevents corrosion and rust on vehicle underbodies and key components.',
            'price': 0.00,
            'image': 'images/rust_protection.jpg'
        },
        {
            'name': 'Paint Protection',
            'description': 'Protects the vehicle’s exterior paint from UV rays, pollutants, and minor abrasions.',
            'price': 0.00,
            'image': 'images/paint_protection.jpg'
        },
        {
            'name': 'Fabric Protection',
            'description': 'Shields fabric and upholstery from stains, spills, and daily wear and tear.',
            'price': 0.00,
            'image': 'images/fabric_protection.jpg'
        },
        {
            'name': 'VIN Etching',
            'description': 'Enhances theft deterrence by etching the vehicle’s VIN on windows and parts.',
            'price': 0.00,
            'image': 'images/vin_etching.jpg'
        },
        {
            'name': 'Extended Warranty',
            'description': 'Provides long-term protection on major vehicle components beyond factory warranty.',
            'price': 0.00,
            'image': 'images/extended_warranty.jpg'
        }
    ]

    # Create products in the database
    for product in core_products:
        Product.objects.create(name=product['name'], description=product['description'], price=product['price'], image=product['image'])
        print(f"Product '{product['name']}' added successfully.")

if __name__ == "__main__":
    add_core_products()
