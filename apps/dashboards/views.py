from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from web_project import TemplateLayout

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
        return context
