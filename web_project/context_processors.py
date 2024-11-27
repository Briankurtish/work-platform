# web_project/context_processors.py
from apps.recharge_account.models import Deposit
from apps.withdraw.models import WithdrawalRequest
from apps.clients.models import Profile
from apps.manage_products.models import Product
from django.db.models import Sum


def pending_counts(request):
    """
    A context processor to add counts of pending deposits and withdrawals to all templates.
    """
    if request.user.is_authenticated:
        # Fetch real-time counts directly from the database
        pending_deposits = Deposit.objects.filter(status='Pending').count()
        pending_withdrawals = WithdrawalRequest.objects.filter(status='pending').count()
        
        total_deposit_amount = Deposit.objects.aggregate(total_amount=Sum('amount'))['total_amount'] or 0
        total_approved_deposit_amount = Deposit.objects.filter(status='Approved').aggregate(total_amount=Sum('amount'))['total_amount'] or 0
        total_approved_withdrawal_amount = WithdrawalRequest.objects.filter(status='approved').aggregate(total_amount=Sum('amount'))['total_amount'] or 0
        total_users = Profile.objects.count()
        total_products = Product.objects.count()
        return {
            'pending_deposits_count': pending_deposits,
            'pending_withdrawals_count': pending_withdrawals,
            'total_deposit_amount': total_deposit_amount,
            'total_approved_deposit_amount': total_approved_deposit_amount,
            'total_approved_withdrawal_amount': total_approved_withdrawal_amount,
            'total_users': total_users,
            'total_products': total_products,
        }
    return {}
