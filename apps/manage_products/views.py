from django.views.generic import TemplateView
from web_project import TemplateLayout
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ProductForm
from .models import Product
from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required




@login_required
def ManageProductView(request):
    products = Product.objects.all()

    # Create a new context dictionary for this view 
    view_context = {
        "products": products,
    }

    # Initialize the template layout and merge the view context
    context = TemplateLayout.init(request, view_context)

    return render(request, 'manage_products.html', context)



@login_required
def add_product_view(request):
    
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('manage-products')
    else:
        form = ProductForm()
    view_context = {
        "form": form,
    }
    context = TemplateLayout.init(request, view_context)

    return render(request, 'add_product.html', context)

@login_required
def delete_product_view(request, pk):
    products = Product.objects.get(id=pk)
    if request.method == "POST":
        products.delete()
        return redirect("manage-products")
    view_context = {
        
    }
    context = TemplateLayout.init(request, view_context)

    return render(request, 'delete_product.html', context)

@login_required
def update_product_view(request, pk):
    products = Product.objects.get(id=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=products)
        if form.is_valid():
            form.save()
            return redirect("manage-products")
    else:
        form = ProductForm(instance=products)
    view_context = {
        "form": form
    }
    context = TemplateLayout.init(request, view_context)

    return render(request, 'update_product.html', context)
