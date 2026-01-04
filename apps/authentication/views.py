from sib_api_v3_sdk import Configuration, ApiClient, TransactionalEmailsApi, SendSmtpEmail
from sib_api_v3_sdk.rest import ApiException
from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,authenticate, logout
from web_project.template_helpers.theme import TemplateHelper
from .forms import CreateUserForm
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth.forms import SetPasswordForm
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib import messages


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
                # Save the form data
                user = form.save()
                username = form.cleaned_data.get('username')
                messages.success(request, f'Account created for {username} successfully. Continue to Log In')
                
                # Send email notifications
                self.send_email_to_client(user)
                self.send_email_to_admin(user)
                
                return redirect('auth-login-basic')
        else:
            form = CreateUserForm()

        # If form is invalid, return the form with errors
        context = {
            'form': form,
            'layout_path': TemplateHelper.set_layout("layout_blank.html", {}),
        }
        return self.render_to_response(context)

    def send_email_to_client(self, user):
        """Send a confirmation email to the client using Hostinger SMTP."""
        try:
            subject = "Welcome to SmartBoostPro"
            sender_email = "SmartBoostPro <info@smartboostpro.com>"  # Add your custom name and email
            recipient_email = user.email
            
            html_content = f"""
            <p>Dear {user.username},</p>
            <p>Welcome to SmartBoostPro! Your account has been successfully created.</p>
            <p>We are excited to have you on board. If you have any questions or need support, feel free to reach out to us.</p>
            <p>Thank you for joining!</p>
            """
            
            # Create an email message object
            email = EmailMessage(
                subject=subject,
                body=html_content,
                from_email=sender_email,  # Custom "From" name with email
                to=[recipient_email],
            )
            email.content_subtype = "html"
            email.send()
        except Exception as e:
            messages.warning(self.request, f"Failed to send email to client: {e}")


    def send_email_to_admin(self, user):
        """Send a notification email to the admin about the new user using Hostinger SMTP."""
        try:
            subject = "New User Registration"
            sender_email = "SmartBoostPro <info@smartboostpro.com>"  # Add your custom name and email
            admin_email = settings.EMAIL_HOST_USER
            
            html_content = f"""
            <p>Dear Admin,</p>
            <p>A new user has registered on SmartBoostPro.</p>
            <p><strong>Username:</strong> {user.username}</p>
            <p><strong>Email:</strong> {user.email}</p>
            <p>Thank you for using SmartBoostPro!</p>
            """
            
            email = EmailMessage(
                subject=subject,
                body=html_content,
                from_email=sender_email,  # Custom "From" name with email
                to=[admin_email],
            )
            email.content_subtype = "html"
            email.send()
        except Exception as e:
            messages.warning(self.request, f"Failed to send email to admin: {e}")

            

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
    

class CustomPasswordResetView(PasswordResetView):
    template_name = 'forgot_password.html'

    def get_context_data(self, **kwargs):
        # Get the default context from the parent class
        context = super().get_context_data(**kwargs)
        # Add the layout_path context variable
        context['layout_path'] = TemplateHelper.set_layout("layout_blank.html", {})
        return context

class CustomPasswordResetViewDone(PasswordResetDoneView):
    template_name = 'forgot_password.html'

    def get_context_data(self, **kwargs):
        # Get the default context from the parent class
        context = super().get_context_data(**kwargs)
        # Add the layout_path context variable
        context['layout_path'] = TemplateHelper.set_layout("layout_blank.html", {})
        return context

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'forgot_password.html'

    def get_context_data(self, **kwargs):
        """
        Add the layout path and the appropriate form to the context.
        """
        # Get the default context from the parent class
        context = super().get_context_data(**kwargs)

        # Add the layout path context variable
        context['layout_path'] = TemplateHelper.set_layout("layout_blank.html", {})

        # Get the user from the kwargs (this is automatically set by Django)
        user = context.get('user')  # This is the user associated with the reset

        # Create the form, passing the user to the form
        context['form'] = SetPasswordForm(user=user)  # Pass the user to the form

        return context
    
class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'forgot_password.html'

    def get_context_data(self, **kwargs):
        # Get the default context from the parent class
        context = super().get_context_data(**kwargs)
        # Add the layout_path context variable
        context['layout_path'] = TemplateHelper.set_layout("layout_blank.html", {})
        return context
