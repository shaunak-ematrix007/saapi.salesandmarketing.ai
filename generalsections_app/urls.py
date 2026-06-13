from django.urls import path
from generalsections_app.sitesettings_views import site_settings_views
from generalsections_app.sitemanagement_views import country_settings_views
from generalsections_app.sitemanagement_views import email_verification_price_views
from generalsections_app.sitemanagement_views import plan_controller_views
from generalsections_app.sitemanagement_views import plan_module_views
from generalsections_app.managemember_views import cancel_registrations_views
from generalsections_app.managemember_views import member_views
from generalsections_app.monthlypricing_views import monthly_pricing_views

urlpatterns = [
    # Site settings routes
    path('settings/getSiteSettings', site_settings_views.get_site_settings, name='get_site_settings'),
    path('settings/updateSiteSettings', site_settings_views.update_site_settings, name='update_site_settings'),

    # Country settings routes
    path('countrySetting/getCountrySettingsById/<int:countrySettingsId>', country_settings_views.get_country_settings_by_id, name='get_country_settings_by_id'),
    path('countrySetting/getCountrySettingsListPage', country_settings_views.get_country_settings_list_page, name='get_country_settings_list_page'),
    path('countrySetting/saveCountrySettings', country_settings_views.save_country_settings, name='save_country_settings'),
    path('countrySetting/deleteCountrySettings', country_settings_views.delete_country_settings, name='delete_country_settings'),
    path('countrySetting/checkDisplayOrder', country_settings_views.check_display_order, name='check_display_order'),
    path('countrySetting/addExpiryDate', country_settings_views.add_expiry_date, name='add_expiry_date'),
    path('countrySetting/getRegistrationLinkLogs', country_settings_views.get_registration_link_logs, name='get_registration_link_logs'),

    # Email verification price routes
    path('emailVerificationPrice/getEmailVerificationPriceList', email_verification_price_views.get_email_verification_price_list, name='get_email_verification_price_list'),
    path('emailVerificationPrice/getEmailVerificationPriceListByCountryId/<int:countryId>', email_verification_price_views.get_email_verification_price_list_by_country_id, name='get_email_verification_price_list_by_country_id'),
    path('emailVerificationPrice/saveEmailVerificationPrice', email_verification_price_views.save_email_verification_price, name='save_email_verification_price'),
    path('emailVerificationPrice/deleteEmailVerificationPrice', email_verification_price_views.delete_email_verification_price, name='delete_email_verification_price'),
    path('emailVerificationPrice/getEmailVerificationPrice/<int:evpId>', email_verification_price_views.get_email_verification_price, name='get_email_verification_price'),

    # Plan routes
    path('plan/getPlanById/<int:countryId>/<int:planId>', plan_controller_views.get_plan_by_id, name='get_plan_by_id'),
    path('plan/getPlanListById/<int:countryId>', plan_controller_views.get_plan_list_by_id, name='get_plan_list_by_id'),
    path('plan/getPlan/<int:planId>', plan_controller_views.get_plan, name='get_plan'),
    path('plan/getPlanList', plan_controller_views.get_plan_list, name='get_plan_list'),
    path('plan/savePlan', plan_controller_views.save_plan, name='save_plan'),
    path('plan/deletePlan', plan_controller_views.delete_plan, name='delete_plan'),
    path('plan/getPlanListCombo', plan_controller_views.get_plan_list_combo, name='get_plan_list_combo'),

    # Plan module routes
    path('planModule/getPlanModule/<int:pmId>', plan_module_views.get_plan_module, name='get_plan_module'),
    path('planModule/getPlanModuleList', plan_module_views.get_plan_module_list, name='get_plan_module_list'),
    path('planModule/getPlanModulePageList', plan_module_views.get_plan_module_page_list, name='get_plan_module_page_list'),
    path('planModule/savePlanModule', plan_module_views.save_plan_module, name='save_plan_module'),
    path('planModule/deletePlanModule', plan_module_views.delete_plan_module, name='delete_plan_module'),

    # Cancel registrations routes
    path('cancelregistrations/getCancelRegistrationsListPage', cancel_registrations_views.get_cancel_registrations_list_page, name='get_cancel_registrations_list_page'),
    path('cancelregistrations/deleteCancelRegistrations', cancel_registrations_views.delete_cancel_registrations, name='delete_cancel_registrations'),

    # Member routes
    path('members/getMemberListPage', member_views.get_member_list_page, name='get_member_list_page'),
    path('members/getMemberById/<int:memberId>', member_views.get_member_by_id, name='get_member_by_id'),
    path('members/deleteMembers', member_views.delete_members, name='delete_members'),
    path('members/saveMember', member_views.save_member, name='save_member'),
    path('members/getTokenByMemberId/<int:memberId>', member_views.get_token_by_member_id, name='get_token_by_member_id'),
    path('members/getDownloadMemberList', member_views.get_download_member_list, name='get_download_member_list'),

    # Monthly Price routes
    path('monthlyPrice/getMonthlyPrice/<int:monthlyPriceId>', monthly_pricing_views.get_monthly_price_by_id, name='get_monthly_price_by_id'),
    path('monthlyPrice/getMonthlyPriceListPage', monthly_pricing_views.get_monthly_price_list_page, name='get_monthly_price_list_page'),
    path('monthlyPrice/saveMonthlyPrice', monthly_pricing_views.save_monthly_price, name='save_monthly_price'),
    path('monthlyPrice/deleteMonthlyPrice', monthly_pricing_views.delete_monthly_price, name='delete_monthly_price'),
]




