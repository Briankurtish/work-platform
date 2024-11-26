from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from web_project import TemplateLayout
from apps.manage_plans.models import Plan

class DashboardsView(LoginRequiredMixin, TemplateView):
    # Default template if no specific role is matched
    template_name = "dashboard_analytics.html"
    
    def get_template_names(self):
        """
        Dynamically select the template based on the user's role:
        - Admins: 'admin_dashboard.html'
        - Staff (non-admin): 'staff_dashboard.html'
        - Regular authenticated users: 'user_dashboard.html'
        """
        if self.request.user.is_authenticated:
            if self.request.user.is_staff and self.request.user.is_superuser:
                # Admin template
                return ["dashboard_admin.html"]
            else:
                # Regular user template
                return ["dashboard_analytics.html"]
        return super().get_template_names()

    def get_context_data(self, **kwargs):
        # Call the parent method and initialize the global layout
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        
        # Fetch the logged-in user's profile and plan
        if hasattr(self.request.user, "profile"):  # Ensure the user has a profile
            profile = self.request.user.profile
            context["user_plan"] = profile.plan  # The plan the user is subscribed to
            context["user_balance"] = profile.balance  # Add the balance to the context
        else:
            context["user_plan"] = None  # No profile or plan
            context["user_balance"] = 0  # If no balance, set it to 0

        return context
