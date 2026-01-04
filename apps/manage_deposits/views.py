from sib_api_v3_sdk import Configuration, ApiClient, TransactionalEmailsApi, SendSmtpEmail
from sib_api_v3_sdk.rest import ApiException
from django.views.generic import TemplateView
from web_project import TemplateLayout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from apps.recharge_account.models import Deposit
from django.db.models import Sum
from django.core.mail import send_mail

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
            subject = "Your Deposit Request Update"
            sender_email = "SmartBoostPro <info@smartboostpro.com>"  # Your Hostinger email
            recipient_email = deposit.user.email  # Dynamically fetch user's email

            # Generate HTML content based on status
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

            # Send email using Django's send_mail function
            send_mail(
                subject,
                "",  # Plain text content (leave empty since we're using HTML)
                sender_email,  # Sender email from Hostinger
                [recipient_email],  # List of recipients
                html_message=html_content,  # HTML content
            )
        except Exception as e:
            # Log error and notify admin or user if needed
            messages.warning(self.request, f"Failed to notify the user: {e}")
