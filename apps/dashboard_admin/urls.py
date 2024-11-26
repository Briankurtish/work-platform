from django.urls import path
from .views import AdminDashboardView

urlpatterns = [
    path(
        "index-admin/",
        AdminDashboardView.as_view(),  # Correct use of as_view()
        name="index-admin",
    )
]
