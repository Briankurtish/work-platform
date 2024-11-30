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

        
    # Send email to admin
        try:
            configuration = sib_api_v3_sdk.Configuration()
            configuration.api_key['api-key'] = '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'  # Replace with your actual API key
            
            api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
            
            subject = "New Deposit Request"
            sender = {"name": "SmartBoostPro", "email": "pbyamungo@gmail.com"}  # Replace with your verified email
            recipient = [{"email": "asaforbrn18@gmail.com"}]  # Admin email
            
            html_content = f"""
            <p>A new deposit request has been submitted:</p>
            <ul>
                <li>User: {user.username}</li>
                <li>Amount: ${amount}</li>
                <li>Crypto Wallet: {crypto_wallet}</li>
            </ul>
            """
            
            send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
                to=recipient,
                sender=sender,
                subject=subject,
                html_content=html_content,
            )
            
            api_instance.send_transac_email(send_smtp_email)
            messages.success(request, "Your recharge request has been submitted successfully.", extra_tags='recharge_account')
        
        except ApiException as e:
            messages.error(request, f"Failed to notify the admin: {e}")

        # Redirect back to the recharge account page
        return redirect('recharge_account')


# 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