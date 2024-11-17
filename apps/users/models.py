from django.db import models
from django.contrib.auth.models import User
from apps.manage_plans.models import Plan
# Create your models here.




class Profile(models.Model):
    client = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    address = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=20, null=True)
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f'{self.client.username} - Profile'
