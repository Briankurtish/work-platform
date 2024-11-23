from django.views.generic import TemplateView
from web_project import TemplateLayout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required




@login_required
def ManageUserView(request):
    products = Product.objects.all()

    # Create a new context dictionary for this view 
    view_context = {
        "products": products,
    }

    # Initialize the template layout and merge the view context
    context = TemplateLayout.init(request, view_context)

    return render(request, 'manage_products.html', context)
