from django.urls import path
from .views import ManageUsersView



urlpatterns = [
    
    path(
        "manage-clients/",
        ManageUsersView,
        name="manage-clients",
    )
]
