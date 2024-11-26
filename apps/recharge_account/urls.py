from django.urls import path
from .views import RechargeAccountView



urlpatterns = [
    
    path(
        "recharge_account/",
        RechargeAccountView.as_view(),
        name="recharge_account",
    )
]
