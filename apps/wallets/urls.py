from django.urls import path
from .views import (
    ManageWalletsView,
    add_wallet_view,
    delete_wallet_view,
    update_wallet_view,
)

urlpatterns = [
    # Wallet Management URLs
    path("manage-wallets/", ManageWalletsView, name="manage-wallets"),
    path("add-wallet/", add_wallet_view, name="add-wallet"),
    path("delete-wallet/<int:pk>/", delete_wallet_view, name="delete-wallet"),
    path("update-wallet/<int:pk>/", update_wallet_view, name="update-wallet"),
]
