from django.urls import path
from dashboard_app.views import dashboard_views

urlpatterns = [
    path('dashboard/getDashboardNewUsers', dashboard_views.get_dashboard_new_users, name='get_dashboard_new_users'),
]
