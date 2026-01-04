from django.urls import path
from .views import WithdrawView, WithdrawDepositView



urlpatterns = [
    
    path(
        "withdraw/",
        WithdrawView.as_view(),
        name="withdraw",
    ),
    path(
        "withdraw-deposit/",
        WithdrawDepositView.as_view(),
        name="withdraw_deposit",
    ),
]
