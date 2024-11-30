from django import forms
from .models import CryptoWallet

class WalletForm(forms.ModelForm):
    class Meta:
        model = CryptoWallet
        fields = ['name', 'network', 'address']