# products/admin.py
from django.contrib import admin
from .models import Product, Plan

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'profit', 'is_super_bonus')  # Columns to display in the admin list view
    list_filter = ('is_super_bonus', 'plans')  # Filters for the admin sidebar
    search_fields = ('name', 'description')  # Searchable fields
    filter_horizontal = ('plans',)  # For managing many-to-many relationships
