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
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from apps.recharge_account.models import Deposit
from apps.manage_products.models import Product
from django.core.mail import send_mail
from django.conf import settings 



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
    Admin view to top up a user's balance and create a pending deposit request.
    """
    if not request.user.is_staff:
        return HttpResponseForbidden("You are not authorized to perform this action.")

    user = get_object_or_404(User, id=user_id)
    profile = get_object_or_404(Profile, client=user)

    if request.method == 'POST':
        form = BalanceTopUpForm(request.POST)
        if form.is_valid():
            balance_top_up = form.cleaned_data['balance_top_up']

            # Create a new deposit request
            Deposit.objects.create(
                user=user,
                amount=balance_top_up,
                crypto_wallet='Admin Top-Up',  # Indicating it's an admin-driven deposit
                status='Pending',
                proof_of_payment=None,
            )

            # Notify the admin via email
            try:
                subject = "New Deposit Request by Admin"
                sender_email = "SmartBoostPro <info@smartboostpro.com>"  
                recipient_email = "info@smartboostpro.com"  # Replace with admin email
                body = f"""
                <p>A new deposit request by Admin has been submitted:</p>
                <ul>
                    <li>User: {request.user.username}</li>
                    <li>Amount: ${amount}</li>
                </ul>
                """
                
                # Send the email using Django's send_mail function
                send_mail(
                    subject,
                    body,
                    sender_email,  # Sender email from settings
                    [recipient_email],  # List of recipients
                    html_message=body,  # HTML content
                )
            except ApiException as e:
                messages.warning(request, f"Failed to send notification email: {e}")

            messages.success(request, f"Balance top-up request for {user.username} has been created and is pending approval.")
            return redirect('manage-clients')
    else:
        form = BalanceTopUpForm()

    context = TemplateLayout.init(request, {'user': user, 'form': form})
    return render(request, 'topup_balance.html', context)


@login_required
def toggle_super_bonus_mode(request, user_id):
    """
    Toggles the 'Super Bonus Mode' for a user's account.
    """
    if not request.user.is_staff:
        return HttpResponseForbidden("You are not authorized to perform this action.")

    user = get_object_or_404(User, id=user_id)
    profile = get_object_or_404(Profile, client=user)

    # Toggle the Super Bonus Mode
    profile.super_bonus_mode = not profile.super_bonus_mode
    profile.save()

    status = "enabled" if profile.super_bonus_mode else "disabled"
    messages.success(request, f"Super Bonus Mode has been {status} for {user.username}.")

    return redirect('manage-clients')


@login_required
def reset_daily_clicks(request, user_id):
    """
    Resets the daily clicks and successful checkouts for the specific user's plan.
    """
    if not request.user.is_staff:
        return HttpResponseForbidden("You are not authorized to perform this action.")
    
    user = get_object_or_404(User, id=user_id)
    profile = get_object_or_404(Profile, client=user)

    if not profile.plan:
        messages.error(request, f"{user.username} does not have an assigned plan.")
        return redirect('manage-clients')

    # Access the plan associated with the user
    plan = profile.plan

    # Reset daily clicks to the plan's number_of_clicks
    plan.daily_clicks = plan.number_of_clicks  # Reset daily clicks to the plan's number_of_clicks
    plan.save()

    # Reset daily checkouts to 0
    profile.daily_checkouts = 0
    profile.save()

    messages.success(request, f"Daily clicks and Daily Boosts for {user.username}'s plan '{plan.name}' have been reset.")
    return redirect('manage-clients')



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