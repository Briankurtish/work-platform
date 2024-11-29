from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ProductForm
from web_project import TemplateLayout
from .models import Product

@login_required
def ManageProductView(request):
    products = Product.objects.all()

    view_context = {
        "products": products,
    }

    context = TemplateLayout.init(request, view_context)

    return render(request, 'manage_products.html', context)


@login_required
def add_product_view(request):
    """
    View to handle the addition of a new product.
    """
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)  # Handle both POST data and file uploads (image)
        if form.is_valid():
            product = form.save()  # Save the product instance (including many-to-many relationships)
            messages.success(request, f"Product {product.name} added successfully.")
            return redirect('manage-products')  # Redirect to the product management page
    else:
        form = ProductForm()  # Instantiate an empty form for GET request

    view_context = {
        "form": form,  # Pass the form to the template
    }
    context = TemplateLayout.init(request, view_context)

    return render(request, 'add_product.html', context)


@login_required
def delete_product_view(request, pk):
    """
    View to handle the deletion of a product.
    """
    product = Product.objects.get(id=pk)  # Get the product by its ID
    if request.method == "POST":
        product.delete()  # Delete the product
        messages.success(request, f"Product {product.name} deleted successfully.")
        return redirect("manage-products")  # Redirect to the product management page

    view_context = {
        "product": product,  # Pass the product to the template for confirmation
    }
    context = TemplateLayout.init(request, view_context)

    return render(request, 'delete_product.html', context)


@login_required
def update_product_view(request, pk):
    """
    View to handle the updating of a product.
    """
    product = Product.objects.get(id=pk)  # Get the product by its ID
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)  # Handle both POST data and file uploads
        if form.is_valid():
            form.save()  # Save the updated product (including many-to-many relationships)
            messages.success(request, f"Product {product.name} updated successfully.")
            return redirect("manage-products")  # Redirect to the product management page
    else:
        form = ProductForm(instance=product)  # Prepopulate the form with the current product data

    view_context = {
        "form": form,  # Pass the form to the template
        "product": product,  # Pass the current product to the template
    }
    context = TemplateLayout.init(request, view_context)

    return render(request, 'update_product.html', context)
