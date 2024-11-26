from django.views.generic import TemplateView
from web_project import TemplateLayout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Plan
from .forms import PlanForm

@login_required
def ManagePlansView(request):
    plans = Plan.objects.all()

    # Create a new context dictionary for this view 
    view_context = {
        "plans": plans,
    }

    # Initialize the template layout and merge the view context
    context = TemplateLayout.init(request, view_context)

    return render(request, 'manage_plans.html', context)



@login_required
def add_plan_view(request):
    
    if request.method == "POST":
        form = PlanForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage-plans')
    else:
        form = PlanForm()
    view_context = {
        "form": form,
    }
    context = TemplateLayout.init(request, view_context)

    return render(request, 'add_plan.html', context)

@login_required
def delete_plan_view(request, pk):
    plans = Plan.objects.get(id=pk)
    if request.method == "POST":
        plans.delete()
        return redirect("manage-plans")
    view_context = {
        
    }
    context = TemplateLayout.init(request, view_context)

    return render(request, 'delete_plan.html', context)

@login_required
def update_plan_view(request, pk):
    plans = Plan.objects.get(id=pk)
    if request.method == "POST":
        form = PlanForm(request.POST, instance=plans)
        if form.is_valid():
            form.save()
            return redirect("manage-plans")
    else:
        form = PlanForm(instance=plans)
    view_context = {
        "form": form
    }
    context = TemplateLayout.init(request, view_context)

    return render(request, 'update_plan.html', context)




# class ManagePlansView(LoginRequiredMixin,TemplateView):
#     # Predefined function
#     def get_context_data(self, **kwargs):
#         # A function to init the global layout. It is defined in web_project/__init__.py file
#         context = TemplateLayout.init(self, super().get_context_data(**kwargs))

#         return context
