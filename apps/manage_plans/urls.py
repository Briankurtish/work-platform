from django.urls import path
from .views import ManagePlansView, add_plan_view, delete_plan_view, update_plan_view



urlpatterns = [
    
    path(
        "manage-plans/", ManagePlansView, name="manage-plans",
    ),
    path("add-plan/", add_plan_view, name="add-plan"),
    path("delete-plan/<int:pk>/", delete_plan_view, name="delete-plan"),
    path("update-plan/<int:pk>/", update_plan_view, name="update-plan"),
]
