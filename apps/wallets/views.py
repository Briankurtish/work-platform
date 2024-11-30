from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from web_project import TemplateLayout
from .models import CryptoWallet
from .forms import WalletForm

@login_required
def ManageWalletsView(request):
    """
    Displays a list of all crypto wallets.
    """
    wallets = CryptoWallet.objects.all()

    # Create a new context dictionary for this view
    view_context = {
        "wallets": wallets,
    }

    # Initialize the template layout and merge the view context
    context = TemplateLayout.init(request, view_context)

    return render(request, 'manage_wallets.html', context)


@login_required
def add_wallet_view(request):
    """
    Handles adding a new crypto wallet.
    """
    if request.method == "POST":
        form = WalletForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage-wallets')
    else:
        form = WalletForm()

    view_context = {
        "form": form,
    }
    context = TemplateLayout.init(request, view_context)

    return render(request, 'add_wallet.html', context)


@login_required
def delete_wallet_view(request, pk):
    """
    Handles deleting a crypto wallet.
    """
    wallet = get_object_or_404(CryptoWallet, id=pk)
    if request.method == "POST":
        wallet.delete()
        return redirect("manage-wallets")

    view_context = {
        "wallet": wallet,
    }
    context = TemplateLayout.init(request, view_context)

    return render(request, 'delete_wallet.html', context)


@login_required
def update_wallet_view(request, pk):
    """
    Handles updating a crypto wallet.
    """
    wallet = get_object_or_404(CryptoWallet, id=pk)
    if request.method == "POST":
        form = WalletForm(request.POST, instance=wallet)
        if form.is_valid():
            form.save()
            return redirect("manage-wallets")
    else:
        form = WalletForm(instance=wallet)

    view_context = {
        "form": form,
    }
    context = TemplateLayout.init(request, view_context)

    return render(request, 'update_wallet.html', context)
