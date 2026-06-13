"""
URL configuration for prod_sam_siteadmin_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path, include

urlpatterns = [
    path('', include('common_app.urls')),
    path('', include('auth_app.urls')),
    path('', include('affiliate_program_app.urls')),
    path('', include('analytics_app.urls')),
    path('', include('dashboard_app.urls')),  # Added for Dashboard module migration
    path('', include('smtp_app.urls')),  # Added for SMTP module migration
    path('', include('subaccount_pages_app.urls')),  # Added for Subaccount Pages module migration
    path('', include('freetemplate_app.urls')),  # Added for Free Template module migration
    path('', include('accounting_app.urls')),  # Added for Invoice, Billing, and Gateway migration
    path('', include('customer_app.urls')),  # Added for Contacts module migration
    path('', include('generalsections_app.urls')),  # Added for General Sections and Site Settings migration
    path('', include('emailCampaigns_app.urls')),  # Added for Email Campaign module migration
]
