from django.urls import path
from .views import admin_dashboard_view

urlpatterns = [
    path(
        "index-admin/",
        admin_dashboard_view,  # Correct use of as_view()
        name="index-admin",
    )
]
