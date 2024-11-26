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

            messages.success(request, f"Your withdrawal request of ${withdrawal_amount} has been submitted for approval.")
            return redirect('withdraw')  # Redirect back to the withdrawal page

        except ValueError:
            # Handle the case where the amount is not a valid number
            messages.error(request, "Invalid withdrawal amount.")
            return redirect('withdraw')  # Redirect back to the withdrawal page