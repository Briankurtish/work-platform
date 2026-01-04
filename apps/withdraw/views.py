from sib_api_v3_sdk import Configuration, ApiClient, TransactionalEmailsApi, SendSmtpEmail
from sib_api_v3_sdk.rest import ApiException
from django.views.generic import TemplateView
from web_project import TemplateLayout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.shortcuts import redirect
from apps.clients.models import Profile  # Import Profile model
from .models import WithdrawalRequest  # Import WithdrawalRequest model
from django.core.mail import send_mail  # Make sure to import send_mail
from django.conf import settings

class WithdrawView(LoginRequiredMixin, TemplateView):
    template_name = "withdraw.html"  # Make sure to specify your template

    def get_context_data(self, **kwargs):
        # Initialize the global layout context
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        # Retrieve the logged-in user's profile
        profile = get_object_or_404(Profile, client=self.request.user)

        # Add the user's profit to the context
        context["user_profit"] = profile.profit
        context["user_balance"] = profile.balance

        # Add crypto wallet choices to the context to be displayed in the template
        # context["crypto_wallet_choices"] = WithdrawalRequest._meta.get_field('crypto_wallet').choices

        return context

    def post(self, request, *args, **kwargs):
        profile = get_object_or_404(Profile, client=request.user)
        withdrawal_amount = request.POST.get('amount')  # Amount the user wants to withdraw
        wallet = request.POST.get('wallet_address')  # Wallet address provided by the user
        crypto_wallet = request.POST.get('crypto_wallet')  # Crypto wallet selection

        # Debugging to check what data is being passed
        print(f"Received wallet_address: {wallet}, crypto_wallet: {crypto_wallet}")

        if not wallet or not crypto_wallet:
            messages.error(request, "Both wallet address and crypto wallet type are required.")
            return redirect('withdraw')  # Redirect back to the withdrawal page

        try:
            # Check if the withdrawal amount is valid
            withdrawal_amount = float(withdrawal_amount)
            if withdrawal_amount <= 0:
                messages.error(request, "Withdrawal amount must be greater than zero.")
                return redirect('withdraw')  # Redirect back to the withdrawal page

            if profile.profit < withdrawal_amount:
                messages.error(request, "Insufficient funds in your account.")
                return redirect('withdraw')  # Redirect back to the withdrawal page

            # Create a WithdrawalRequest object (status will be 'pending' by default)
            withdrawal_request = WithdrawalRequest.objects.create(
                user=request.user,
                amount=withdrawal_amount,
                wallet=wallet,
                crypto_wallet=crypto_wallet,
            )

            # Send email notification to admin
            try:
                subject = "New Withdrawal Request"
                sender_email = "SmartBoostPro <info@smartboostpro.com>"  
                recipient_email = "info@smartboostpro.com"  # Replace with admin email
                body = f"""
                <p>A new withdrawal request has been submitted:</p>
                <ul>
                    <li>User: {request.user.username}</li>
                    <li>Amount: ${withdrawal_amount}</li>
                    <li>Wallet Address: {wallet}</li>
                    <li>Crypto Wallet: {crypto_wallet}</li>
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
                
            except Exception as e:
                messages.warning(request, f"Failed to notify admin about the withdrawal request: {e}")

            # Notify user of success
            messages.success(request, f"Your withdrawal request of ${withdrawal_amount} has been submitted for approval.")
            return redirect('withdraw')

        except ValueError:
            messages.error(request, "Invalid withdrawal amount.")
            return redirect('withdraw')
        

class WithdrawDepositView(LoginRequiredMixin, TemplateView):
    template_name = "withdraw_deposit.html"  # Make sure to specify your template

    def get_context_data(self, **kwargs):
        # Initialize the global layout context
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        # Retrieve the logged-in user's profile
        profile = get_object_or_404(Profile, client=self.request.user)

        # Add the user's profit to the context
        context["user_profit"] = profile.profit
        context["user_balance"] = profile.balance

        # Add crypto wallet choices to the context to be displayed in the template
        # context["crypto_wallet_choices"] = WithdrawalRequest._meta.get_field('crypto_wallet').choices

        return context

    def post(self, request, *args, **kwargs):
        profile = get_object_or_404(Profile, client=request.user)
        withdrawal_amount = request.POST.get('amount')  # Amount the user wants to withdraw
        wallet = request.POST.get('wallet_address')  # Wallet address provided by the user
        crypto_wallet = request.POST.get('crypto_wallet')  # Crypto wallet selection

        # Debugging to check what data is being passed
        print(f"Received wallet_address: {wallet}, crypto_wallet: {crypto_wallet}")

        if not wallet or not crypto_wallet:
            messages.error(request, "Both wallet address and crypto wallet type are required.")
            return redirect('withdraw_deposit')  # Redirect back to the withdrawal page

        try:
            # Check if the withdrawal amount is valid
            withdrawal_amount = float(withdrawal_amount)
            if withdrawal_amount <= 0:
                messages.error(request, "Withdrawal amount must be greater than zero.")
                return redirect('withdraw_deposit')  # Redirect back to the withdrawal page

            if profile.balance < withdrawal_amount:
                messages.error(request, "Insufficient funds in your account.")
                return redirect('withdraw_deposit')  # Redirect back to the withdrawal page

            # Create a WithdrawalRequest object (status will be 'pending' by default)
            withdrawal_request = WithdrawalRequest.objects.create(
                user=request.user,
                amount=withdrawal_amount,
                wallet=wallet,
                crypto_wallet=crypto_wallet,
            )

            # Send email notification to admin
            try:
                subject = "New Balance Withdrawal Request"
                sender_email = "SmartBoostPro <info@smartboostpro.com>"  
                recipient_email = "info@smartboostpro.com"  # Replace with admin email
                body = f"""
                <p>A new withdrawal request has been submitted:</p>
                <ul>
                    <li>User: {request.user.username}</li>
                    <li>Amount: ${withdrawal_amount}</li>
                    <li>Wallet Address: {wallet}</li>
                    <li>Crypto Wallet: {crypto_wallet}</li>
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
                
            except Exception as e:
                messages.warning(request, f"Failed to notify admin about the withdrawal request: {e}")

            # Notify user of success
            messages.success(request, f"Your Balance withdrawal request of ${withdrawal_amount} has been submitted for approval.")
            return redirect('withdraw_deposit')

        except ValueError:
            messages.error(request, "Invalid withdrawal amount.")
            return redirect('withdraw_deposit')