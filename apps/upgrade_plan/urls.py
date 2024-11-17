from django.urls import path
from .views import UpgradePlanView



urlpatterns = [
    
    path(
        "upgrade-plan/",
        UpgradePlanView.as_view(template_name="upgrade_plan.html"),
        name="upgrade-plan",
    )
]
