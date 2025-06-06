# Generated by Django 3.2.25 on 2025-04-05 04:53

import Apps.C3_app1.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('C3_app1', '0014_alter_product_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sale',
            name='status',
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, default=Apps.C3_app1.models.default_product_image, upload_to='products/'),
        ),
        migrations.AlterField(
            model_name='sale',
            name='date_added',
            field=models.DateField(auto_now_add=True),
        ),
    ]
