from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from web_project import TemplateLayout
from django.contrib import messages
from .models import Deposit


class RechargeAccountView(LoginRequiredMixin, TemplateView):
    template_name = "recharge_account.html"

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
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

        # Show success message and redirect
        messages.success(request, "Your recharge request has been submitted successfully.", extra_tags='recharge_account')
        return redirect('recharge_account')
