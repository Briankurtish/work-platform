from django.db import models
from django.contrib.auth.models import User
from apps.clients.models import Profile

class WithdrawalRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    wallet = models.CharField(max_length=255, blank=False) 
    crypto_wallet = models.CharField(max_length=255, blank=False) 
    status_choices = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=10, choices=status_choices, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    rejected_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Withdrawal Request by {self.user.username} for ${self.amount} to {self.wallet}"
