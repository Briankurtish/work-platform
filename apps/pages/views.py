from django.views.generic import TemplateView
from web_project import TemplateLayout
from apps.authentication.forms import UserUpdateForm, ProfileUpdateForm
from django.shortcuts import render, redirect
from django.contrib import messages


"""
This file is a view controller for multiple pages as a module.
Here you can override the page view layout.
Refer to pages/urls.py file for more pages.
"""


class PagesView(TemplateView):
    # Predefined function
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        # Create forms for user and profile updates
        user_form = UserUpdateForm(instance=self.request.user)
        profile_form = ProfileUpdateForm(instance=self.request.user.profile)  # Assuming Profile model is linked to User

        context['user_form'] = user_form
        context['profile_form'] = profile_form
        return context
    
    # Handle POST request to update user and profile data
    def post(self, request, *args, **kwargs):
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, instance=request.user.profile)  # Assuming Profile model is linked to User

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your account has been updated successfully!')
            return redirect('pages-account-settings-account')  # Redirect to a relevant page (e.g., profile page)
        else:
            messages.error(request, 'Please correct the errors below.')
            return self.render_to_response(self.get_context_data(user_form=user_form, profile_form=profile_form))
