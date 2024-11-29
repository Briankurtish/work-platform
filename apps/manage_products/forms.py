from django import forms
from .models import Product, Plan

class ProductForm(forms.ModelForm):
    # Create a field for selecting multiple plans
    plans = forms.ModelMultipleChoiceField(
        queryset=Plan.objects.all(),  # Get all plans from the database
        widget=forms.CheckboxSelectMultiple,  # Display as checkboxes
        required=False,  # It's not required to select plans
        label="Select Plans"  # Label for the field
    )

    class Meta:
        model = Product
        fields = ['name', 'image', 'price', 'profit', 'description', 'is_super_bonus', 'plans']  # Include 'plans' field
