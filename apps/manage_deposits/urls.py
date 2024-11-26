from django.urls import path
from .views import ManageDepositsView

urlpatterns = [
    path('manage-deposits/', ManageDepositsView.as_view(), name='manage-deposits'),
]
