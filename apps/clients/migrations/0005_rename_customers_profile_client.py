# Generated by Django 5.0.6 on 2024-11-23 06:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0004_rename_profile_profile_customers'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='customers',
            new_name='client',
        ),
    ]
