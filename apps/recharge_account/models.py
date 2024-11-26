from django.db import models
from django.contrib.auth.models import User

class Deposit(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="deposits")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    crypto_wallet = models.CharField(max_length=50, choices=[
        ('Bitcoin - BTC', 'Bitcoin - BTC'),
        ('USDT - TRC20', 'USDT - TRC20'),
        ('Etherium - ERC-20', 'Etherium - ERC-20'),
    ])
    proof_of_payment = models.FileField(upload_to='proof_of_payment/')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.amount} ({self.status})"
