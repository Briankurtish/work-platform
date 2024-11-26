from django.urls import path
from .views import UpgradePlanView



urlpatterns = [
    
    path(
        "upgrade_plan/",
        UpgradePlanView.as_view(),
        name="upgrade_plan",
    )
]
