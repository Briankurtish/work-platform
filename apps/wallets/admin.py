from django.contrib import admin
from .models import CryptoWallet

@admin.register(CryptoWallet)
class CryptoWalletAdmin(admin.ModelAdmin):
    list_display = ('name', 'network', 'address')  # Fields to display in the admin list view
    search_fields = ('name', 'network', 'address')  # Fields to enable search functionality
    list_filter = ('network',)  # Fields to filter by in the admin sidebar
