from django.views.generic import TemplateView
from web_project import TemplateLayout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from apps.recharge_account.models import Deposit

class ManageDepositsView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "manage_deposits.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Initialize the global layout
        context = TemplateLayout.init(self, context)

        # Fetch all deposit requests from the database
        context['deposits'] = Deposit.objects.all().order_by('-created_at')
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
            elif action == 'reject':
                if deposit.status != 'Pending':
                    messages.warning(request, "This deposit has already been processed.")
                else:
                    deposit.status = 'Rejected'
                    deposit.save()
                    messages.success(request, "Deposit rejected successfully.")
            else:
                messages.error(request, "Invalid action.")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")

        return redirect('manage-deposits')
