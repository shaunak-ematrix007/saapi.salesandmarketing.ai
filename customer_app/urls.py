from django.urls import path
from customer_app.managegroups_views import manage_group_views
from customer_app.managecustomer_views import contact_import_views, customer_views, group_views, group_segment_views

urlpatterns = [
    # Manage Group Routes
    path('manageGroup/getGroup/<int:groupId>', manage_group_views.get_group, name='get_group'),
    path('manageGroup/deleteGroups', manage_group_views.delete_groups, name='delete_groups'),
    path('manageGroup/getGroupListPage/', manage_group_views.get_group_list_page, name='get_group_list_page'),
    path('manageGroup/exportGroup/<int:groupId>/<int:memberId>', manage_group_views.get_download_contact_file, name='get_download_contact_file'),

    # Contact Import Routes
    path('contactImport', contact_import_views.import_contact, name='import_contact'),
    path('contactImport/headerFieldMapping', contact_import_views.get_header_field_mapping, name='get_header_field_mapping'),
    path('contactImport/selectHeaders', contact_import_views.get_selected_headers, name='get_selected_headers'),
    path('contactImport/addTempCronContact', contact_import_views.add_temp_cron_contact, name='add_temp_cron_contact'),
    path('contactImport/updateImportContact', contact_import_views.update_import_contact, name='update_import_contact'),
    path('contactImport/contactImportFile', contact_import_views.import_contact_file, name='import_contact_file'),

    # Customer Module Routes
    path('manageCustomer/importContact', contact_import_views.import_contact_by_admin_side, name='import_contact_by_admin_side'),
    path('manageCustomer/getCustomerListPage/', customer_views.get_customer_list_page, name='get_customer_list_page'),
    path('manageCustomer/getCustomerListPage/<str:searchKey>', customer_views.get_customer_list_page, name='get_customer_list_page_with_search'),
    path('manageCustomer/deleteCustomers', customer_views.delete_customers, name='delete_customers'),

    # Group Module Routes
    path('group/getGroupList', group_views.get_group_list, name='get_group_list'),
    path('group/getGroupById/<int:groupId>', group_views.get_group, name='get_group_by_id'),
    path('group/saveGroup', group_views.save_group, name='save_group'),
    path('group/deleteBulkGroup', group_views.delete_bulk_group, name='delete_bulk_group'),
    path('group/getGroupUDFList/<int:groupId>', group_views.get_udf_list, name='get_group_udf_list'),
    path('group/getGroupUDFValueList/<int:groupId>/<str:groupUDF>', group_views.get_udf_value_list, name='get_group_udf_value_list'),
    path('group/getGroupContactHeader/<int:groupId>', group_views.get_group_contact_header, name='get_group_contact_header'),
    path('group/getGroupContactHeaderKey/<int:groupId>', group_views.get_group_contact_header_key, name='get_group_contact_header_key'),
    path('group/inviteByUrl', group_views.invite_by_url, name='invite_by_url'),
    path('group/getInviteByUrlData', group_views.get_invite_by_url_data, name='get_invite_by_url_data'),
    path('group/getGroupUDF/<int:groupId>', group_views.get_group_udf, name='get_group_udf'),
    path('group/getGroupFirstRecords/<int:groupId>', group_views.get_group_first_records, name='get_group_first_records'),

    # Group Segment Module Routes
    path('groupSegment/addSegment', group_segment_views.create_group_segment, name='create_group_segment'),
    path('groupSegment/updateSegment/<int:segmentId>', group_segment_views.update_group_segment, name='update_group_segment'),
    path('groupSegment/getSegment/<int:segmentId>', group_segment_views.get_segment, name='get_segment'),
    path('groupSegment/getSegmentList/<int:groupId>', group_segment_views.get_segment_list, name='get_segment_list'),
    path('groupSegment/deleteBulkSegment', group_segment_views.delete_bulk_segment, name='delete_bulk_segment'),
    path('groupSegment/getSegmentContactList/<int:groupId>/<int:segmentId>/', group_segment_views.get_segment_contact_list, name='get_segment_contact_list'),
]
