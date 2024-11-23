from django.urls import path
from .views import ManageProductView, add_product_view, delete_product_view, update_product_view



urlpatterns = [
    
    path(
        "manage-products/", ManageProductView, name="manage-products",
    ),
    path("add-product/", add_product_view, name="add-product"),
    path("delete-product/<int:pk>/", delete_product_view, name="delete-product"),
    path("update-product/<int:pk>/", update_product_view, name="update-product"),
]
