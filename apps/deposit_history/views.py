from django.views.generic import TemplateView
from web_project import TemplateLayout
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.recharge_account.models import Deposit  # Assuming Deposit model is in this app

class DepositHistoryView(LoginRequiredMixin, TemplateView):
    template_name = "deposit_history.html"  # Your HTML template to render the deposit history

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Initialize the global layout
        context = TemplateLayout.init(self, context)

        # Fetch the current user
        user = self.request.user

        # Fetch all deposits made by the user, excluding Admin Top-Up records
        context['deposits'] = (
            Deposit.objects.filter(user=user)
            .exclude(crypto_wallet="Admin Top-Up")
            .order_by('-created_at')
        )

        return context
