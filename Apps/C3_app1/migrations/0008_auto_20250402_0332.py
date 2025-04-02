# Generated by Django 3.2.25 on 2025-04-02 03:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('C3_app1', '0007_alter_sale_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='dealership',
        ),
        migrations.RemoveField(
            model_name='product',
            name='stock',
        ),
        migrations.RemoveField(
            model_name='sale',
            name='dealership',
        ),
        migrations.RemoveField(
            model_name='sale',
            name='product_sold',
        ),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stock', models.PositiveIntegerField(default=0)),
                ('dealership', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='C3_app1.dealership')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='C3_app1.product')),
            ],
            options={
                'unique_together': {('product', 'dealership')},
            },
        ),
        migrations.AddField(
            model_name='sale',
            name='inventory',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='C3_app1.inventory'),
            preserve_default=False,
        ),
    ]
