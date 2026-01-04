import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from web_project import TemplateLayout
from django.contrib import messages
from .models import Deposit
from apps.wallets.models import CryptoWallet
from django.core.mail import send_mail
from django.conf import settings 


class RechargeAccountView(LoginRequiredMixin, TemplateView):
    template_name = "recharge_account.html"

    def get_context_data(self, **kwargs):
        # Fetch crypto wallets from the database
        wallets = CryptoWallet.objects.all()
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['wallets'] = wallets  # Add wallets to context
        return context

    def post(self, request, *args, **kwargs):
        # Get form data
        user = request.user
        amount = request.POST.get('amount')
        crypto_wallet = request.POST.get('crypto_wallet')
        proof_of_payment = request.FILES.get('proof_of_payment')

        # Validate input
        if not amount or not crypto_wallet or not proof_of_payment:
            messages.error(request, "All fields are required.")
            return redirect('recharge_account')

        # Create a new deposit
        Deposit.objects.create(
            user=user,
            amount=amount,
            crypto_wallet=crypto_wallet,
            proof_of_payment=proof_of_payment,
        )

        
        # Send email notification to admin
        try:
            subject = "New Deposit Request"
            sender_email = "SmartBoostPro <info@smartboostpro.com>"  
            recipient_email = "info@smartboostpro.com"  # Replace with admin email
            body = f"""
            <p>A new deposit request has been submitted:</p>
            <ul>
                <li>User: {request.user.username}</li>
                <li>Amount: ${amount}</li>
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
            messages.warning(request, f"Failed to notify admin about the deposit request: {e}")

        # Redirect back to the recharge account page
        return redirect('recharge_account')


# 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