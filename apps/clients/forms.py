from django import forms
from .models import Profile

class BalanceTopUpForm(forms.ModelForm):
    """
    Form for topping up the user's balance.
    """
    balance_top_up = forms.DecimalField(
        max_digits=10, decimal_places=2, required=True,
        label="Balance Top-Up Amount",
        widget=forms.NumberInput(attrs={'placeholder': 'Enter amount'}),
    )

    class Meta:
        model = Profile
        fields = []

class ProfitTopUpForm(forms.ModelForm):
    """
    Form for topping up the user's profit.
    """
    profit_top_up = forms.DecimalField(
        max_digits=10, decimal_places=2, required=True,
        label="Profit Top-Up Amount",
        widget=forms.NumberInput(attrs={'placeholder': 'Enter amount'}),
    )

    class Meta:
        model = Profile
        fields = []
