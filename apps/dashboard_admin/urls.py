from django.urls import path
from .views import AdminDashboardView



urlpatterns = [
    
    path(
        "index-admin/",
        AdminDashboardView.as_view(template_name="dashboard_admin.html"),
        name="index-admin",
    )
]
