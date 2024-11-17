from django.urls import path
from .views import ManageProductsView



urlpatterns = [
    
    path(
        "manage-products/",
        ManageProductsView.as_view(template_name="manage_products.html"),
        name="manage-products",
    )
]
