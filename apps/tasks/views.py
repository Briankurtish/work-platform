from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.views.generic import TemplateView
from django.db.models import Sum
from apps.recharge_account.models import Deposit
from apps.manage_plans.models import Plan
from apps.manage_products.models import Product
from apps.withdraw.models import WithdrawalRequest
from web_project import TemplateLayout
from django.contrib.auth.mixins import LoginRequiredMixin


class TasksView(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        # Initialize the global layout
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        
        # Fetch the logged-in user's profile and plan
        if hasattr(self.request.user, "profile"):  # Ensure the user has a profile
            user = self.request.user
            profile = self.request.user.profile
            
            if profile.plan is None:
                # If the user has no plan, set appropriate context
                context["user_plan"] = None
                context["random_product"] = None
                context["no_plan_message"] = "You are not subscribed to any plan. Please subscribe to a plan to view products."
            else:
                # Calculate totals and clicks left
                context['total_approved_deposits'] = (
                    Deposit.objects.filter(user=user, status='Approved').aggregate(total=Sum('amount'))['total'] or 0
                )
                context['total_approved_withdrawals'] = (
                    WithdrawalRequest.objects.filter(user=user, status='approved').aggregate(total=Sum('amount'))['total'] or 0
                )
                context["user_profit"] = profile.profit
                context["successful_checkouts"] = profile.successful_checkouts
                context["clicks_left"] = profile.plan.daily_clicks - profile.successful_checkouts
                context["user_plan"] = profile.plan

                # Track previously selected products in session
                selected_products = self.request.session.get("selected_products", [])

                # Filter products based on Super Bonus Mode or plan-specific criteria
                if profile.super_bonus_mode:
                    # Show only products with `is_super_bonus` set to True
                    products = Product.objects.filter(is_super_bonus=True).exclude(id__in=selected_products).order_by('?')
                else:
                    # Show products based on the user's plan
                    if profile.plan.name == 'VIP 1':
                        products = Product.objects.filter(is_super_bonus=False, price__lte=100).exclude(id__in=selected_products).order_by('?')
                    elif profile.plan.name == 'VIP 2':
                        products = Product.objects.filter(is_super_bonus=False, price__lte=500).exclude(id__in=selected_products).order_by('?')
                    elif profile.plan.name == 'VIP 3':
                        products = Product.objects.filter(is_super_bonus=False, price__lte=2000).exclude(id__in=selected_products).order_by('?')
                    elif profile.plan.name == 'VIP 4':
                        products = Product.objects.filter(is_super_bonus=False, price__gte=5000).exclude(id__in=selected_products).order_by('?')
                    else:
                        # Default behavior for other plans (show all non-super bonus products)
                        products = Product.objects.filter(is_super_bonus=False).exclude(id__in=selected_products).order_by('?')

                # Select a random product
                random_product = products.first() if products.exists() else None
                context["random_product"] = random_product

                if random_product:
                    # Update session with the newly selected product ID
                    selected_products.append(random_product.id)
                    self.request.session["selected_products"] = selected_products
                if not products.exists():
                    # Reset session if no products remain
                    self.request.session["selected_products"] = []
        else:
            # Handle case where the user has no profile
            context["user_plan"] = None
            context["random_product"] = None
        
        return context

    def post(self, request, *args, **kwargs):
        # Get product ID from the form submission
        product_id = request.POST.get('product_id')
        
        if not product_id:
            return HttpResponseForbidden("Product ID is missing.")
        
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            messages.error(request, "Product not found.")
            return redirect('task-panel')
        
        user_profile = request.user.profile
        user_balance = Deposit.objects.filter(user=request.user, status='Approved').aggregate(total=Sum('amount'))['total'] or 0
        
        # Check if the user has enough balance to proceed with the checkout
        if user_balance < product.price:
            messages.error(request, "Insufficient balance to boost this product. Please Recharge your account!")
            return redirect('task-panel')
        
        # Check if the user has reached the maximum number of successful checkouts for today
        if user_profile.successful_checkouts >= user_profile.plan.daily_clicks:
            messages.error(request, "You have reached the maximum number of boosts for today.")
            return redirect('task-panel')

        # Proceed with the checkout
        user_profile.profit += product.profit
        user_profile.successful_checkouts += 1
        user_profile.save()

        messages.success(request, f"Successfully Boosted the product: {product.name}. Commission added!")

        return redirect('task-panel')
