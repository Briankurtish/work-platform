from django.urls import path
from .views import UsersView



urlpatterns = [
    
    path(
        "users-list/",
        UsersView.as_view(template_name="user-list.html"),
        name="users",
    )
]
