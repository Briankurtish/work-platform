# Generated by Django 5.0.6 on 2024-11-29 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manage_plans', '0002_plan_number_of_clicks'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='daily_clicks',
            field=models.PositiveIntegerField(default=0),
        ),
    ]