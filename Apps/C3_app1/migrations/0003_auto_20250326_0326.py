# Generated by Django 3.2.25 on 2025-03-26 03:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('C3_app1', '0002_claim_sales'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sales',
            old_name='text',
            new_name='name',
        ),
        migrations.AddField(
            model_name='sales',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sales',
            name='product',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sales',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user', null=True, blank=True),
            preserve_default=False,
        ),
    ]
