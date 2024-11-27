from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.clients.models import Profile
from apps.withdraw.models import WithdrawalRequest
from apps.recharge_account.models import Deposit
from apps.manage_products.models import Product
from django.db.models import Sum
from web_project import TemplateLayout

@login_required
def admin_dashboard_view(request):
    # Initialize context
    context = {}

    # Add global template layout
    context = TemplateLayout.init(request, context)

    # Fetch data for the dashboard

    # Total Users
    context['total_users'] = Profile.objects.count()

    # Total Deposits
    context['total_deposits'] = Deposit.objects.count()
    context['total_deposit_amount'] = Deposit.objects.aggregate(total_amount=Sum('amount'))['total_amount'] or 0

    # Total Approved Deposits
    context['total_approved_deposits'] = Deposit.objects.filter(status='Approved').count()
    context['total_approved_deposit_amount'] = Deposit.objects.filter(status='Approved').aggregate(total_amount=Sum('amount'))['total_amount'] or 0

    # Total Pending Deposits
    context['total_pending_deposits'] = Deposit.objects.filter(status='Pending').count()
    context['total_pending_deposit_amount'] = Deposit.objects.filter(status='Pending').aggregate(total_amount=Sum('amount'))['total_amount'] or 0

    # Total Withdrawals
    context['total_withdrawals'] = WithdrawalRequest.objects.count()
    context['total_withdrawal_amount'] = WithdrawalRequest.objects.aggregate(total_amount=Sum('amount'))['total_amount'] or 0

    # Total Approved Withdrawals
    context['total_approved_withdrawals'] = WithdrawalRequest.objects.filter(status='approved').count()
    context['total_approved_withdrawal_amount'] = WithdrawalRequest.objects.filter(status='approved').aggregate(total_amount=Sum('amount'))['total_amount'] or 0

    # Total Pending Withdrawals
    context['total_pending_withdrawals'] = WithdrawalRequest.objects.filter(status='pending').count()
    context['total_pending_withdrawal_amount'] = WithdrawalRequest.objects.filter(status='pending').aggregate(total_amount=Sum('amount'))['total_amount'] or 0

    # Total Products
    context['total_products'] = Product.objects.count()

    # Render the template with the context
    return render(request, "dashboard_admin.html", context)
