from django.urls import path
from .views import ManageUsersView, deactivate_user, activate_user, delete_user
from . import views


urlpatterns = [
    # Manage Users View
    path(
        "manage-clients/",
        ManageUsersView,
        name="manage-clients",
    ),
    
    path('top-up-balance/<int:user_id>/', views.top_up_balance, name='top_up_balance'),
    path('top-up-profit/<int:user_id>/', views.top_up_profit, name='top_up_profit'),
    
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
