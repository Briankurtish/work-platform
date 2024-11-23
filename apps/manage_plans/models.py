from django.db import models

# Create your models here.
class Plan(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    profit = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    number_of_clicks = models.PositiveIntegerField(default=10)

    def __str__(self):
        return self.name