from django.urls import path
from .views import ManageDepositsView



urlpatterns = [
    
    path(
        "manage-deposits/",
        ManageDepositsView.as_view(template_name="manage_deposits.html"),
        name="manage-deposits",
    )
]
