from django.urls import path
from .views import ManageUsersView, deactivate_user, activate_user, delete_user

urlpatterns = [
    # Manage Users View
    path(
        "manage-clients/",
        ManageUsersView,
        name="manage-clients",
    ),
    
    # Deactivate User
    path(
        "deactivate-user/<int:user_id>/",
        deactivate_user,
        name="deactivate-user",
    ),
    
    path("activate-user/<int:user_id>/", activate_user, name="activate-user"),

    # You can add a delete user path here if needed
    path("delete-user/<int:user_id>/", delete_user, name="delete-user"),
]
