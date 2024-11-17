# Generated by Django 5.0.6 on 2024-11-17 21:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manage_plans', '0001_initial'),
        ('users', '0002_plan_profile_plan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='plan',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='manage_plans.plan'),
        ),
        migrations.DeleteModel(
            name='Plan',
        ),
    ]
