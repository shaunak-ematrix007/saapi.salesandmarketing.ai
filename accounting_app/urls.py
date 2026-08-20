from django.urls import path
from accounting_app.views import invoice_views, uninvoice_views

urlpatterns = [
    path('invoiced/getInvoiceListPage/', invoice_views.get_invoice_list_page, name='get_invoice_list_page'),
    path('invoiced/printInvoice', invoice_views.print_invoice, name='print_invoice'),
    path('invoiced/createInvoice/<int:member_id>', invoice_views.create_invoice, name='create_invoice'),
    path('uninvoiced/getUninvoiceMembers', uninvoice_views.get_uninvoice_members, name='get_uninvoice_members'),
    path('uninvoiced/getUninvoiceListPage', uninvoice_views.get_uninvoice_list_page, name='get_uninvoice_list_page'),
    path('uninvoiced/getUninvoiceListPageWithId/', uninvoice_views.get_uninvoice_list_page_with_id, name='get_uninvoice_list_page_with_id'),
]
