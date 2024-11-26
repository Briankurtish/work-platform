from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,authenticate, logout
from web_project.template_helpers.theme import TemplateHelper
from .forms import CreateUserForm


"""
This file is a view controller for multiple pages as a module.
Here you can override the page view layout.
Refer to auth/urls.py file for more pages.
"""

class AuthView(TemplateView):
    template_name = 'user/auth.html'  # The template to render for this view

    def get(self, request, *args, **kwargs):
        """
        Display the registration form on GET request.
        """
        form = CreateUserForm()
        context = {
            'form': form,
            'layout_path': TemplateHelper.set_layout("layout_blank.html", {}),
        }
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        """
        Handle form submission on POST request.
        """
        
        if request.method == "POST":
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                messages.success(request, f'Account created for {username} successfully. Continue to Log In')
                return redirect('auth-login-basic')
        else:
            form = CreateUserForm()
        

        # If form is invalid, return the form with errors
        context = {
            'form': form,
            'layout_path': TemplateHelper.set_layout("layout_blank.html", {}),
        }
        return self.render_to_response(context)



class LoginView(TemplateView):
    template_name = 'user/login.html'  # The template to render for this view

    def get(self, request, *args, **kwargs):
        """
        Display the login form on GET request.
        """
        form = AuthenticationForm()
        context = {
            'form': form,
            'layout_path': TemplateHelper.set_layout("layout_blank.html", {}),
        }
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        """
        Handle form submission on POST request.
        """
        if request.method == "POST":
            form = AuthenticationForm(data=request.POST)
            if form.is_valid():
                # Authenticate the user
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    # Log the user in
                    login(request, user)
                    messages.success(request, f'Welcome back, {user.username}!')
                    return redirect('index')  # Redirect to homepage after login
                else:
                    messages.error(request, 'Invalid username or password.')
            else:
                messages.error(request, 'Please correct the errors below.')

        else:
            form = AuthenticationForm()

        context = {
            'form': form,
            'layout_path': TemplateHelper.set_layout("layout_blank.html", {}),
        }
        return self.render_to_response(context)
    
    

class LogoutView(TemplateView):
    """
    Logs the user out and redirects them to the login page or home page.
    """
    template_name = 'user/logout.html'  # Optional, if you want to show a logout page

    def get(self, request, *args, **kwargs):
        """
        Log the user out and redirect to the login page or index page.
        """
        logout(request)
        messages.info(request, "You have been logged out successfully.")
        return redirect('auth-login-basic')  # Redirect to login page or home page (adjust the URL as necessary)