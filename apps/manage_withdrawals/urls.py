from django.urls import path
from .views import ManageWithdrawalsView



urlpatterns = [
    
    path(
        "manage-withdrawals/",
        ManageWithdrawalsView.as_view(template_name="manage_withdrawals.html"),
        name="manage-withdrawals",
    )
]
