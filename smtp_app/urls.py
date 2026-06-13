from django.urls import path
from smtp_app.views import smtp_views

urlpatterns = [
    path('smtpServer/saveSmtpServer', smtp_views.save_smtp_server, name='save_smtp_server'),
    path('smtpServer/getSmtpServer/<int:smtpId>', smtp_views.get_smtp_server, name='get_smtp_server'),
    path('smtpServer/deleteSmtpServer/<int:smtpId>', smtp_views.delete_smtp_server, name='delete_smtp_server'),
    path('smtpServer/getAllSmtpServers', smtp_views.get_all_smtp_servers, name='get_all_smtp_servers'),
]
