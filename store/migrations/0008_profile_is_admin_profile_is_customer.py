# Generated by Django 5.0.4 on 2024-05-16 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_profile_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='profile',
            name='is_customer',
            field=models.BooleanField(default=False),
        ),
    ]