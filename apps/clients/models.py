from django.db import models
from django.contrib.auth.models import User as UserModel
from apps.manage_plans.models import Plan as PlanModel
# Create your models here.




class Profile(models.Model):
    client = models.OneToOneField(UserModel, on_delete=models.CASCADE, null=True)
    address = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=20, null=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    plan = models.ForeignKey(PlanModel, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f'{self.client.username} - Profile'