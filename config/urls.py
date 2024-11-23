"""
URL configuration for web_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
from web_project.views import SystemView
from django.contrib.auth import views as auth_views
from django.conf import settings

from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),
    
    # path(
    #     "auth/login/",
    #     auth_views.LoginView.as_view(template_name="auth_login_basic.html"),
    #     name="auth-login-basic",
    # ),

    # Dashboard urls
    path("", include("apps.dashboards.urls")),
    
    # Admin Dashboard urls
    path("", include("apps.dashboard_admin.urls")),
    
    # Task Panel urls
    path("", include("apps.tasks.urls")),
    
    # User List urls
    path("", include("apps.users.urls")),
    
    # Manage Deposits urls
    path("", include("apps.manage_deposits.urls")),
    
    # Manage Withdrawals urls
    path("", include("apps.manage_withdrawals.urls")),
    
    # Manage Plans urls
    path("", include("apps.manage_plans.urls")),
    
    # Manage Products urls
    path("", include("apps.manage_products.urls")),
    
    # Recharge accounts urls
    path("", include("apps.recharge_account.urls")),
    
    # Withdraw urls
    path("", include("apps.withdraw.urls")),
    
    # Upgrade Plan urls
    path("", include("apps.upgrade_plan.urls")),
    
    # Withdrawal History urls
    path("", include("apps.withdrawal_history.urls")),
    
    # Deposit History urls
    path("", include("apps.deposit_history.urls")),

    # layouts urls
    path("", include("apps.layouts.urls")),

    # Pages urls
    path("", include("apps.pages.urls")),

    # Auth urls
    path("", include("apps.authentication.urls")),

    # Card urls
    path("", include("apps.cards.urls")),

    # UI urls
    path("", include("apps.ui.urls")),

    # Extended UI urls
    path("", include("apps.extended_ui.urls")),

    # Icons urls
    path("", include("apps.icons.urls")),

    # Forms urls
    path("", include("apps.forms.urls")),

    # FormLayouts urls
    path("", include("apps.form_layouts.urls")),

    # Tables urls
    path("", include("apps.tables.urls")),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = SystemView.as_view(template_name="pages_misc_error.html", status=404)
handler400 = SystemView.as_view(template_name="pages_misc_error.html", status=400)
handler500 = SystemView.as_view(template_name="pages_misc_error.html", status=500)
