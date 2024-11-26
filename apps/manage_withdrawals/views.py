from django.views.generic import TemplateView
from web_project import TemplateLayout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from apps.withdraw.models import WithdrawalRequest  # Assuming WithdrawalRequest model
from apps.clients.models import Profile  # Assuming Profile model

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
            elif action == 'reject':
                # Reject the withdrawal request
                withdrawal.status = 'rejected'
                withdrawal.save()
                messages.success(request, f"Withdrawal request for ${withdrawal.amount} rejected.")
            else:
                messages.error(request, "Invalid action.")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")

        return redirect('manage-withdrawals')
