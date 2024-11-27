from sib_api_v3_sdk import Configuration, ApiClient, TransactionalEmailsApi, SendSmtpEmail
from sib_api_v3_sdk.rest import ApiException
from django.views.generic import TemplateView
from web_project import TemplateLayout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from apps.recharge_account.models import Deposit
from django.db.models import Sum

class ManageDepositsView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "manage_deposits.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Initialize the global layout
        context = TemplateLayout.init(self, context)

        # Fetch all deposit requests from the database
        context['deposits'] = Deposit.objects.all().order_by('-created_at')
        context['total_deposits'] = Deposit.objects.count()
        context['total_deposit_amount'] = Deposit.objects.aggregate(total_amount=Sum('amount'))['total_amount'] or 0
        # Total Approved Deposits
        context['total_approved_deposits'] = Deposit.objects.filter(status='Approved').count()
        context['total_approved_deposit_amount'] = Deposit.objects.filter(status='Approved').aggregate(total_amount=Sum('amount'))['total_amount'] or 0
        return context

    def test_func(self):
        # Ensure the user is an admin
        return self.request.user.is_staff or self.request.user.is_superuser

    def post(self, request, *args, **kwargs):
        # Get the deposit ID and action (approve or reject) from the POST data
        deposit_id = request.POST.get('deposit_id')
        action = request.POST.get('action')

        try:
            # Fetch the deposit object
            deposit = get_object_or_404(Deposit, id=deposit_id)

            # Ensure the user has a profile associated
            if not hasattr(deposit.user, 'profile'):
                messages.error(request, "User profile not found.")
                return redirect('manage-deposits')

            profile = deposit.user.profile  # Access the user's profile

            if action == 'approve':
                if deposit.status != 'Pending':
                    messages.warning(request, "This deposit has already been processed.")
                else:
                    deposit.status = 'Approved'
                    profile.balance += deposit.amount  # Update the profile's balance
                    deposit.save()
                    profile.save()
                    messages.success(request, "Deposit approved successfully.")

                    # Send email notification to the user about the approval
                    self.notify_user(deposit, "approved")

            elif action == 'reject':
                if deposit.status != 'Pending':
                    messages.warning(request, "This deposit has already been processed.")
                else:
                    deposit.status = 'Rejected'
                    deposit.save()
                    messages.success(request, "Deposit rejected successfully.")

                    # Send email notification to the user about the rejection
                    self.notify_user(deposit, "rejected")

            else:
                messages.error(request, "Invalid action.")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")

        return redirect('manage-deposits')

    def notify_user(self, deposit, status):
        """Send notification email to the user about the deposit status."""
        try:
            configuration = Configuration()
            configuration.api_key['api-key'] = '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'  # Replace with your actual API key
            
            api_instance = TransactionalEmailsApi(ApiClient(configuration))
            subject = "Your Deposit Request Update"
            sender = {"name": "SmartBoostPro", "email": "pbyamungo@gmail.com"}  # Replace with your verified email
            recipient = [{"email": deposit.user.email}]  # Dynamically get user's email
            
            if status == "approved":
                html_content = f"""
                <p>Dear {deposit.user.username},</p>
                <p>Your deposit request of <strong>${deposit.amount}</strong> has been approved.</p>
                <p>Your updated balance is <strong>${deposit.user.profile.balance}</strong>.</p>
                """
            elif status == "rejected":
                html_content = f"""
                <p>Dear {deposit.user.username},</p>
                <p>Unfortunately, your deposit request of <strong>${deposit.amount}</strong> has been rejected.</p>
                """
            
            send_smtp_email = SendSmtpEmail(
                to=recipient,
                sender=sender,
                subject=subject,
                html_content=html_content,
            )
            
            api_instance.send_transac_email(send_smtp_email)
        except ApiException as e:
            messages.warning(self.request, f"Failed to notify the user: {e}")
