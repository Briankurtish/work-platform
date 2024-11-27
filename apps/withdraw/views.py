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

class WithdrawView(LoginRequiredMixin, TemplateView):
    template_name = "withdraw.html"  # Make sure to specify your template

    def get_context_data(self, **kwargs):
        # Initialize the global layout context
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        # Retrieve the logged-in user's profile
        profile = get_object_or_404(Profile, client=self.request.user)

        # Add the user's profit to the context
        context["user_profit"] = profile.profit

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
                configuration = Configuration()
                configuration.api_key['api-key'] = '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'  # Replace with your actual API key
                
                api_instance = TransactionalEmailsApi(ApiClient(configuration))
                subject = "New Withdrawal Request"
                sender = {"name": "SmartBoostPro", "email": "pbyamungo@gmail.com"}  # Replace with verified email
                recipient = [{"email": "asaforbrn18@gmail.com"}] # Replace with admin email
                
                html_content = f"""
                <p>A new withdrawal request has been submitted:</p>
                <ul>
                    <li>User: {request.user.username}</li>
                    <li>Amount: ${withdrawal_amount}</li>
                    <li>Wallet Address: {wallet}</li>
                    <li>Crypto Wallet: {crypto_wallet}</li>
                </ul>
                """
                
                send_smtp_email = SendSmtpEmail(
                    to=recipient,
                    sender=sender,
                    subject=subject,
                    html_content=html_content,
                )
                
                api_instance.send_transac_email(send_smtp_email)
            except ApiException as e:
                messages.warning(request, f"Failed to notify admin about the withdrawal request: {e}")

            # Notify user of success
            messages.success(request, f"Your withdrawal request of ${withdrawal_amount} has been submitted for approval.")
            return redirect('withdraw')

        except ValueError:
            messages.error(request, "Invalid withdrawal amount.")
            return redirect('withdraw')