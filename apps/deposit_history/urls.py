from django.urls import path
from .views import DepositHistoryView



urlpatterns = [
    
    path(
        "deposit-history/",
        DepositHistoryView.as_view(template_name="deposit_history.html"),
        name="deposit-history",
    )
]
