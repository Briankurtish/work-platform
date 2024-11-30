from django.urls import path
from .views import AuthView, LoginView, LogoutView, CustomPasswordResetView, CustomPasswordResetViewDone, CustomPasswordResetConfirmView, CustomPasswordResetCompleteView
from django.contrib.auth import views as auth_views



urlpatterns = [
    path(
        "",
        LoginView.as_view(template_name="auth_login_basic.html"),
        name="auth-login-basic",
    ),
    path(
        "auth/register/",
        AuthView.as_view(template_name="auth_register_basic.html"),
        name="auth-register-basic",
    ),
    # Password reset URLs - Django's built-in views
     path('password_reset/', CustomPasswordResetView.as_view(template_name = 'forgot_password.html'), name='password_reset'),
    path('password_reset/done/', CustomPasswordResetViewDone.as_view(template_name = 'reset_password_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(template_name = "reset_password.html"), name='password_reset_confirm'),
    path('reset/done/', CustomPasswordResetCompleteView.as_view(template_name = 'reset_password_complete.html'), name='password_reset_complete'),
    
    path(
        "auth/logout/",
        LogoutView.as_view(template_name="logout.html"),
        name="logout",
    ),
]
