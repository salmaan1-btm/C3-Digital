# Generated by Django 3.2.25 on 2025-03-27 02:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('C3_app1', '0002_auto_20250326_1906'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='dealership',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='C3_app1.dealership'),
        ),
    ]
