from django.urls import path
from analytics_app.views import analytics_event

urlpatterns = [
    path('analytics/getDevicesUsersCampaigns', analytics_event.get_devices_users_campaigns, name='get_devices_users_campaigns'),
    path('analytics/getSessionPageLogData', analytics_event.get_session_page_log_data, name='get_session_page_log_data'),
    path('analytics/getDashboardData', analytics_event.get_dashboard_data, name='get_dashboard_data'),
    path('analytics/getMinuteActiveUsers', analytics_event.get_minute_active_users, name='get_minute_active_users'),
    path('analytics/getPageLogData', analytics_event.get_page_log_data, name='get_page_log_data'),
    path('analytics/getCountryLogData', analytics_event.get_country_log_data, name='get_country_log_data'),
]
