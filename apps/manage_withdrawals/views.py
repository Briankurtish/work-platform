from django.views.generic import TemplateView
from web_project import TemplateLayout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from apps.withdraw.models import WithdrawalRequest  # Assuming WithdrawalRequest model
from apps.clients.models import Profile  # Assuming Profile model
from sib_api_v3_sdk import Configuration, ApiClient, TransactionalEmailsApi, SendSmtpEmail
from sib_api_v3_sdk.rest import ApiException
from django.core.mail import send_mail

class ManageWithdrawalsView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "manage_withdrawals.html"  # Your template for managing withdrawals

    def get_context_data(self, **kwargs):
        # Initialize the global layout
        context = super().get_context_data(**kwargs)
        context = TemplateLayout.init(self, context)

        # Fetch all withdrawal requests from the database and order by creation time
        context['withdrawals'] = WithdrawalRequest.objects.all().order_by('-created_at')
        return context

    def test_func(self):
        # Ensure the user is an admin (staff or superuser)
        return self.request.user.is_staff or self.request.user.is_superuser

    def post(self, request, *args, **kwargs):
        # Get the withdrawal ID and action (approve or reject) from the POST data
        withdrawal_id = request.POST.get('withdrawal_id')
        action = request.POST.get('action')

        try:
            # Fetch the withdrawal object by ID
            withdrawal = get_object_or_404(WithdrawalRequest, id=withdrawal_id)

            # Ensure the withdrawal request status is 'pending' before action
            if withdrawal.status != 'pending':
                messages.warning(request, "This withdrawal request has already been processed.")
                return redirect('manage-withdrawals')

            # Fetch the user's profile (associated with the withdrawal request)
            profile = get_object_or_404(Profile, client=withdrawal.user)

            if action == 'approve':
                # Approve the withdrawal request
                withdrawal.status = 'approved'
                profile.profit -= withdrawal.amount  # Deduct the amount from the user's profit
                withdrawal.save()
                profile.save()
                messages.success(request, f"Withdrawal of ${withdrawal.amount} approved successfully.")

                # Send email notification to the user about the approval
                self.notify_user(withdrawal, "approved")

            elif action == 'reject':
                # Reject the withdrawal request
                withdrawal.status = 'rejected'
                withdrawal.save()
                messages.success(request, f"Withdrawal request for ${withdrawal.amount} rejected.")

                # Send email notification to the user about the rejection
                self.notify_user(withdrawal, "rejected")

            else:
                messages.error(request, "Invalid action.")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")

        return redirect('manage-withdrawals')

    def notify_user(self, withdrawal, status):
        """Send notification email to the user about the withdrawal status."""
        try:
            subject = "Your Withdrawal Request Update"
            sender_email = "SmartBoostPro <info@smartboostpro.com>"  # Your Hostinger email
            recipient_email = withdrawal.user.email  # Dynamically fetch user's email

            # Generate HTML content based on status
            if status == "approved":
                html_content = f"""
                <p>Dear {withdrawal.user.username},</p>
                <p>Your withdrawal request of <strong>${withdrawal.amount}</strong> has been approved.</p>
                <p>Your updated balance is <strong>${withdrawal.user.profile.profit}</strong>.</p>
                """
            elif status == "rejected":
                html_content = f"""
                <p>Dear {withdrawal.user.username},</p>
                <p>Unfortunately, your withdrawal request of <strong>${withdrawal.amount}</strong> has been rejected.</p>
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