import os
import django

# Set up Django settings before importing models
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "C3_Website.settings")

# Initialize Django
django.setup()

# Now import your models after setting up Django settings
from Apps.C3_app1.models import Product

# Image credits
# https://www.noxudolusa.com/wp-content/uploads/2017/06/rustproofing-your-car.jpg
# https://www.bemac.ca/wp-content/uploads/2022/05/Paint-Protection-Film-1024x683.jpg
# https://masterguardsa.co.za/wp-content/uploads/2017/10/fibre_protect.jpg
# https://www.instaetch.com/images/high%20resolution%20vin%20etching.jpg
# https://www.carpro.com/hs-fs/hubfs/extended-warranty-shutterstock.jpg?width=1020&name=extended-warranty-shutterstock.jpg

def add_core_products():
    core_products = [
        {
            'name': 'Rust Protection',
            'description': 'Prevents corrosion and rust on vehicle underbodies and key components.',
            'price': 150.00,
            'image': 'rust_protection.jpg'
        },
        {
            'name': 'Paint Protection',
            'description': 'Protects the vehicle’s exterior paint from UV rays, pollutants, and minor abrasions.',
            'price': 300.00,
            'image': 'paint_protection.jpg'
        },
        {
            'name': 'Fabric Protection',
            'description': 'Shields fabric and upholstery from stains, spills, and daily wear and tear.',
            'price': 100.00,
            'image': 'fabric_protection.jpg'
        },
        {
            'name': 'VIN Etching',
            'description': 'Enhances theft deterrence by etching the vehicle’s VIN on windows and parts.',
            'price': 50.00,
            'image': 'vin_etching.jpg'
        },
        {
            'name': 'Extended Warranty',
            'description': 'Provides long-term protection on major vehicle components beyond factory warranty.',
            'price': 1250.00,
            'image': 'extended_warranty.jpg'
        }
    ]

    # Create products in the database
    for product in core_products:
        Product.objects.create(name=product['name'], description=product['description'], price=product['price'], image=product['image'])
        print(f"Product '{product['name']}' added successfully.")

if __name__ == "__main__":
    add_core_products()
