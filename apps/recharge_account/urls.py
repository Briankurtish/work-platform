from django.urls import path
from .views import RechargeAccountView



urlpatterns = [
    
    path(
        "recharge-account/",
        RechargeAccountView.as_view(template_name="recharge_account.html"),
        name="recharge-account",
    )
]
