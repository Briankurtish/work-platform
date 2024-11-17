from django.urls import path
from .views import WithdrawalHistoryView



urlpatterns = [
    
    path(
        "withdrawal-history/",
        WithdrawalHistoryView.as_view(template_name="withdrawal_history.html"),
        name="withdrawal-history",
    )
]
