# plans/admin.py
from django.contrib import admin
from .models import Plan

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'profit', 'number_of_clicks')  # Columns for the Plan model
    search_fields = ('name',)  # Searchable fields
