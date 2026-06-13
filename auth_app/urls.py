# REMINDER: Include this file in site_admin/prod_sam_siteadmin_api/prod_sam_siteadmin_api/urls.py
# by adding: path('adminUser/', include('auth_app.urls')),

from django.urls import path
from auth_app.views import admin_views, admin_pages_views, admin_user_type_views

urlpatterns = [
    # Admin User endpoints
    path('adminUser/getAdmin/<int:adminId>', admin_views.get_admin_by_id, name='get_admin_by_id'),
    path('adminUser/deleteAdmin', admin_views.delete_admin, name='delete_admin'),
    path('adminUser/saveAdmin', admin_views.save_admin, name='save_admin'),
    path('adminUser/token', admin_views.token, name='token'),
    path('adminUser/changePassword', admin_views.change_password, name='change_password'),
    path('adminUser/getAdminListPage', admin_views.get_admin_list_page, name='get_admin_list_page'),
    
    # Admin Pages and Permissions endpoints
    path('adminPages/saveAdminPage', admin_pages_views.save_admin_page, name='save_admin_page'),
    path('adminPages/getAdminPage/<int:pgId>', admin_pages_views.get_admin_page, name='get_admin_page'),
    path('adminPages/getAdminPageDetails/<int:pgId>', admin_pages_views.get_admin_page_details, name='get_admin_page_details'),
    path('adminPages/getAdminPageList', admin_pages_views.get_admin_page_list, name='get_admin_page_list'),
    path('adminPages/deleteAdminPage', admin_pages_views.delete_admin_page, name='delete_admin_page'),
    
    # Admin User Types (Roles) endpoints
    path('adminType/saveAdminUserType', admin_user_type_views.save_admin_user_type, name='save_admin_user_type'),
    path('adminType/getAdminUserType/<int:id>', admin_user_type_views.get_admin_user_type, name='get_admin_user_type'),
    path('adminType/getAdminUserTypeListPage', admin_user_type_views.get_admin_user_type_list_page, name='get_admin_user_type_list_page'),
    path('adminType/deleteAdminUserType', admin_user_type_views.delete_admin_user_type, name='delete_admin_user_type'),
]
