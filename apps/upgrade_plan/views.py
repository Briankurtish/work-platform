from django.views.generic import TemplateView
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from web_project import TemplateLayout

from django.contrib.auth.mixins import LoginRequiredMixin
from apps.manage_plans.models import Plan  # Import the Plan model
from apps.clients.models import Profile  # Adjust based on your project structure

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
        except ValueError as e:
            messages.error(request, str(e))
        
        return redirect("upgrade_plan")  # Redirect back to the same page
