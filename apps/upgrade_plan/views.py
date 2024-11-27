from django.views.generic import TemplateView
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from web_project import TemplateLayout
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.manage_plans.models import Plan  # Import the Plan model
from apps.clients.models import Profile  # Adjust based on your project structure
from sib_api_v3_sdk import Configuration, ApiClient, TransactionalEmailsApi, SendSmtpEmail
from sib_api_v3_sdk.rest import ApiException
from django.conf import settings

class UpgradePlanView(LoginRequiredMixin, TemplateView):
    template_name = "upgrade_plan.html"  # Replace with the actual template file

    def get_context_data(self, **kwargs):
        # Initialize the global layout
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        # Fetch all plans from the database
        context['plans'] = Plan.objects.all()

        return context

    def post(self, request, *args, **kwargs):
        """
        Handle plan subscription.
        """
        # Get the plan ID from the form submission
        plan_id = request.POST.get("plan_id")
        
        if not plan_id:
            messages.error(request, "No plan selected. Please try again.")
            return redirect("upgrade_plan")  # Replace with the correct view name
        
        # Fetch the selected plan
        plan = get_object_or_404(Plan, id=plan_id)

        # Get the user's profile
        profile = request.user.profile  # Assuming Profile is linked to User with OneToOneField

        # Subscribe the user to the selected plan
        try:
            profile.subscribe_to_plan(plan)  # Use the method defined in the Profile model
            messages.success(request, "You have successfully upgraded your plan.", extra_tags='plan_upgrade')

            # Send an email notification to the user about the new subscription
            self.notify_user(profile, plan)
        except ValueError as e:
            messages.error(request, str(e))
        
        return redirect("upgrade_plan")  # Redirect back to the same page

    def notify_user(self, profile, plan):
        """Send a notification email to the user about the plan they subscribed to."""
        try:
            # Set up the email configuration
            configuration = Configuration()
            configuration.api_key['api-key'] = settings.BREVO_API_KEY  # Replace with your actual API key
            
            api_instance = TransactionalEmailsApi(ApiClient(configuration))
            subject = "Your Subscription Plan Update"
            sender = {"name": "SmartBoostPro", "email": "pbyamungo@gmail.com"}  # Replace with your verified email
            recipient = [{"email": profile.client.email}]  # Dynamically get the user's email
            
            html_content = f"""
            <p>Dear {profile.client.username},</p>
            <p>You have successfully subscribed to the <strong>{plan.name}</strong> plan.</p>
            <p>Your new plan will take effect immediately, and we hope it helps you reach your goals.</p>
            <p>If you have any questions, feel free to contact our support team.</p>
            <p>Thank you for being a part of our community!</p>
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
