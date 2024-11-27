from django.views.generic import TemplateView
from web_project import TemplateLayout
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.recharge_account.models import Deposit
from apps.withdraw.models import WithdrawalRequest
from apps.manage_plans.models import Plan
from apps.manage_products.models import Product
import random
from django.db.models import Sum




"""
This file is a view controller for multiple pages as a module.
Here you can override the page view layout.
Refer to dashboards/urls.py file for more pages.
"""


class TasksView(LoginRequiredMixin,TemplateView):
    # Predefined function
    def get_context_data(self, **kwargs):
        # A function to init the global layout. It is defined in web_project/__init__.py file
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        
        # Fetch the logged-in user's profile and plan
        if hasattr(self.request.user, "profile"):  # Ensure the user has a profile
            user = self.request.user
            profile = self.request.user.profile
            
            # Total approved deposits
            context['total_approved_deposits'] = (
                Deposit.objects.filter(user=user, status='Approved').aggregate(total=Sum('amount'))['total'] or 0
            )
            
            # Add the user's profit to the context
            context["user_profit"] = profile.profit
            
            # Total approved withdrawals
            context['total_approved_withdrawals'] = (
                WithdrawalRequest.objects.filter(user=user, status='approved').aggregate(total=Sum('amount'))['total'] or 0
            )
            context["user_plan"] = profile.plan
            
           # Fetch one random non-super bonus product
            products = Product.objects.filter(is_super_bonus=False).order_by('?')  # Randomize with database
            context["random_product"] = products.first() if products.exists() else None
        
        else:
            context["user_plan"] = None  # No profile or plan
            

        
        return context
