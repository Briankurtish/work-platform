from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.withdraw.models import WithdrawalRequest  # Import the WithdrawalRequest model
from web_project import TemplateLayout

class WithdrawalHistoryView(LoginRequiredMixin, TemplateView):
    template_name = "withdrawal_history.html"  # Make sure to specify your template name

    def get_context_data(self, **kwargs):
        # Initialize the global layout context
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        # Fetch all withdrawal requests made by the logged-in user
        withdrawals = WithdrawalRequest.objects.filter(user=self.request.user).order_by('-created_at')

        # Add withdrawals to the context
        context["withdrawals"] = withdrawals

        return context
