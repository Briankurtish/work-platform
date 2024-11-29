
from django.db import models
from apps.manage_plans.models import Plan

class Product(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='products/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    profit = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    is_super_bonus = models.BooleanField(default=False)  # Toggle for Super Bonus Products

    # Many-to-Many relationship with Plan
    plans = models.ManyToManyField(Plan, related_name='products')

    def __str__(self):
        return self.name