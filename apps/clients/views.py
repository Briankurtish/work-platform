from django.shortcuts import render
from django.views.generic import TemplateView
from web_project import TemplateLayout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required



# Create your views here.
@login_required
def ManageUsersView(request):
    clients = User.objects.all().select_related('profile')

    # Create a new context dictionary for this view 
    view_context = {
        "clients": clients,
    }

    # Initialize the template layout and merge the view context
    context = TemplateLayout.init(request, view_context)

    return render(request, 'manage-users.html', context)