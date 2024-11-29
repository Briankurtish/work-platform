from django.shortcuts import render
from django.views.generic import TemplateView
from web_project import TemplateLayout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponseForbidden
from .forms import BalanceTopUpForm, ProfitTopUpForm
from .models import Profile



# Create your views here.
@login_required
def ManageUsersView(request):
    # Fetch users who are not superusers
    clients = User.objects.filter(is_superuser=False).select_related('profile')

    # Create a new context dictionary for this view 
    view_context = {
        "clients": clients,
    }

    # Initialize the template layout and merge the view context
    context = TemplateLayout.init(request, view_context)

    return render(request, 'manage-users.html', context)


@login_required
def activate_user(request, user_id):
    """
    Activates the user's account.
    """
    user = get_object_or_404(User, id=user_id)
    
    if not user.is_active:
        user.is_active = True
        user.save()
        messages.success(request, f'User {user.username} has been activated.')
    else:
        messages.info(request, f'User {user.username} is already active.')
    
    return redirect('manage-clients')  # Redirect back to the users list


@login_required
def deactivate_user(request, user_id):
    """
    Deactivates a user account by setting `is_active` to False.
    """
    if not request.user.is_staff:
        messages.error(request, "You are not authorized to perform this action.")
        return redirect('manage-users')

    user = get_object_or_404(User, id=user_id)

    if user.is_active:
        user.is_active = False
        user.save()
        messages.success(request, f"{user.username}'s account has been deactivated.")
    else:
        messages.warning(request, f"{user.username}'s account is already inactive.")

    return redirect('manage-clients')


@login_required
def delete_user(request, user_id):
    """
    Displays a confirmation page to delete a user and deletes the user upon confirmation.
    """
    user = get_object_or_404(User, id=user_id)
    
    # Check if the current user has permission to delete
    if not request.user.is_staff:
        return HttpResponseForbidden("You are not authorized to delete this user.")
    
    if request.method == 'POST':
        # You may want to delete the associated profile as well
        if hasattr(user, 'profile'):
            user.profile.delete()  # Delete related profile if needed
        
        # Delete the user account
        user.delete()
        messages.success(request, f'User {user.username} has been deleted.')
        return redirect('manage-clients')  # Redirect back to the users list
    
    
    view_context = {
        'user': user
    }
    
    context = TemplateLayout.init(request, view_context)
    
    return render(request, 'delete_user.html', context)


@login_required
def top_up_balance(request, user_id):
    """
    View for topping up a user's balance.
    """
    if not request.user.is_staff:
        return HttpResponseForbidden("You are not authorized to perform this action.")

    user = get_object_or_404(User, id=user_id)
    profile = get_object_or_404(Profile, client=user)

    if request.method == 'POST':
        form = BalanceTopUpForm(request.POST)
        if form.is_valid():
            balance_top_up = form.cleaned_data['balance_top_up']
            profile.balance += balance_top_up
            profile.save()
            messages.success(request, f"Successfully topped up {user.username}'s balance by {balance_top_up}.")
            return redirect('manage-clients')
    else:
        form = BalanceTopUpForm()

    view_context = {'user': user, 'form': form}
    context = TemplateLayout.init(request, view_context)

    return render(request, 'topup_balance.html', context)


@login_required
def top_up_profit(request, user_id):
    """
    View for topping up a user's profit.
    """
    if not request.user.is_staff:
        return HttpResponseForbidden("You are not authorized to perform this action.")

    user = get_object_or_404(User, id=user_id)
    profile = get_object_or_404(Profile, client=user)

    if request.method == 'POST':
        form = ProfitTopUpForm(request.POST)
        if form.is_valid():
            profit_top_up = form.cleaned_data['profit_top_up']
            profile.profit += profit_top_up
            profile.save()
            messages.success(request, f"Successfully topped up {user.username}'s profit by {profit_top_up}.")
            return redirect('manage-clients')
    else:
        form = ProfitTopUpForm()

    view_context = {'user': user, 'form': form}
    context = TemplateLayout.init(request, view_context)

    return render(request, 'topup_profit.html', context)