# Generated by Django 3.2.25 on 2025-04-02 23:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('C3_app1', '0009_rename_stock_inventory_quantity'),
    ]

    operations = [
        migrations.CreateModel(
            name='Support',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('subject', models.CharField(max_length=200)),
                ('message', models.TextField()),
            ],
        ),
    ]
