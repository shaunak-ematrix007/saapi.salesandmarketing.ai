from django.urls import path
from emailCampaigns_app.views import email_campaign_views, email_campaign_report_views, email_campaign_ab_testing_report_views

urlpatterns = [
    # Email Campaign endpoints
    path('emailCampaign/getCampaignWiseEmailCampaignList', email_campaign_views.get_campaign_wise_email_campaign_list, name='get_campaign_wise_email_campaign_list'),
    path('emailCampaign/getServerWiseEmailCampaignList', email_campaign_views.get_server_wise_email_campaign_list, name='get_server_wise_email_campaign_list'),
    path('emailCampaign/getContactListByCampId', email_campaign_views.get_contact_list_by_camp_id, name='get_contact_list_by_camp_id'),
    path('emailCampaign/getServerListByCampId/<int:campSendId>', email_campaign_views.get_server_list_by_camp_id, name='get_server_list_by_camp_id'),
    path('emailCampaign/reassignServer', email_campaign_views.reassign_server, name='reassign_server'),
    path('emailCampaign/getArchiveEmailCampaignList', email_campaign_views.get_archive_email_campaign_list, name='get_archive_email_campaign_list'),

    # Email Campaign Report endpoints
    path('emailCampaignReport/getEmailCampaignsReportListPage', email_campaign_report_views.get_email_campaigns_report_list_page, name='get_email_campaigns_report_list_page'),
    path('emailCampaignReport/getEmailCampaignsReportDashboard', email_campaign_report_views.get_email_campaigns_report_dashboard, name='get_email_campaigns_report_dashboard'),
    path('emailCampaignReport/getBouncedEmailReportList', email_campaign_report_views.get_bounced_email_report_list, name='get_bounced_email_report_list'),
    path('emailCampaignReport/getEmailCampaignsReportProductLinks', email_campaign_report_views.get_email_campaigns_report_product_links, name='get_email_campaigns_report_product_links'),
    path('emailCampaignReport/getEmailCampaignsReportProductLinksClickUser', email_campaign_report_views.get_email_campaigns_report_product_links_click_user, name='get_email_campaigns_report_product_links_click_user'),
    path('emailCampaignReport/getEmailCampaignsReportMembersListPage', email_campaign_report_views.get_email_campaigns_report_members_list_page, name='get_email_campaigns_report_members_list_page'),
    path('emailCampaignReport/getEmailCampaignsReportMemberClick', email_campaign_report_views.get_email_campaigns_report_member_click, name='get_email_campaigns_report_member_click'),
    path('emailCampaignReport/getEmailCampaignsReportMembersList', email_campaign_report_views.get_email_campaigns_report_members_list, name='get_email_campaigns_report_members_list'),
    path('emailCampaignReport/getEmailCampaignsReportSources', email_campaign_report_views.get_email_campaigns_report_sources, name='get_email_campaigns_report_sources'),
    path('emailCampaignReport/getCampaignsReportPrint', email_campaign_report_views.get_campaigns_report_print, name='get_campaigns_report_print'),

    # Email Campaign A/B Testing Report endpoints
    path('emailCampaignAbTestingReport/getEmailCampaignsReportDashboardAB', email_campaign_ab_testing_report_views.get_email_campaigns_report_dashboard_ab, name='get_email_campaigns_report_dashboard_ab'),
    path('emailCampaignAbTestingReport/getEmailCampaignsReportProductLinksAB', email_campaign_ab_testing_report_views.get_email_campaigns_report_product_links_ab, name='get_email_campaigns_report_product_links_ab'),
    path('emailCampaignAbTestingReport/getEmailCampaignsReportMembersListPageAB', email_campaign_ab_testing_report_views.get_email_campaigns_report_members_list_page_ab, name='get_email_campaigns_report_members_list_page_ab'),
    path('emailCampaignAbTestingReport/getEmailCampaignsReportMembersBListPageAB', email_campaign_ab_testing_report_views.get_email_campaigns_report_members_b_list_page_ab, name='get_email_campaigns_report_members_b_list_page_ab'),
    path('emailCampaignAbTestingReport/getEmailCampaignsReportMembersOListPageAB', email_campaign_ab_testing_report_views.get_email_campaigns_report_members_o_list_page_ab, name='get_email_campaigns_report_members_o_list_page_ab'),
    path('emailCampaignAbTestingReport/getEmailCampaignsReportSourcesAB', email_campaign_ab_testing_report_views.get_email_campaigns_report_sources_ab, name='get_email_campaigns_report_sources_ab'),
    path('emailCampaignAbTestingReport/getCampaignsReportPrintAB', email_campaign_ab_testing_report_views.get_campaigns_report_print_ab, name='get_campaigns_report_print_ab'),
    path('emailCampaignAbTestingReport/setChooseWinner', email_campaign_ab_testing_report_views.set_choose_winner, name='set_choose_winner'),
    path('emailCampaignAbTestingReport/getEmailCampaignsReportMembersListAB', email_campaign_ab_testing_report_views.get_email_campaigns_report_members_list_ab, name='get_email_campaigns_report_members_list_ab'),
]

