# REMINDER: Remember to include this routing file in the main urls.py file:
# D:\py_qa_final\prod\site_admin\prod_sam_siteadmin_api\prod_sam_siteadmin_api\urls.py
# by adding: path('', include('subaccount_pages_app.urls'))

from django.urls import path
from subaccount_pages_app.views import subaccount_pages_views

urlpatterns = [
    path('subaccountPages/saveSubaccountPage', subaccount_pages_views.save_subaccount_page, name='save_subaccount_page'),
    path('subaccountPages/getSubaccountPage/<int:pgId>', subaccount_pages_views.get_subaccount_page, name='get_subaccount_page'),
    path('subaccountPages/getSubaccountPageDetails/<int:pgId>', subaccount_pages_views.get_subaccount_page_details, name='get_subaccount_page_details'),
    path('subaccountPages/getSubaccountPageList/', subaccount_pages_views.get_subaccount_page_list, name='get_subaccount_page_list'),
    path('subaccountPages/deleteSubaccountPage', subaccount_pages_views.delete_subaccount_page, name='delete_subaccount_page'),
]
