# Generated by Django 3.2.25 on 2025-04-02 03:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('C3_app1', '0008_auto_20250402_0332'),
    ]

    operations = [
        migrations.RenameField(
            model_name='inventory',
            old_name='stock',
            new_name='quantity',
        ),
    ]
