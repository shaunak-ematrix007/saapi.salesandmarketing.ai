from django.urls import path
from common_app.views import common_views

urlpatterns = [
    path('lookupdata', common_views.lookup_data, name='lookup_data'),
    path('sendingEmail', common_views.sending_email, name='sending_email'),
    path('displayLanguage', common_views.display_language, name='display_language'),
    path('language', common_views.language, name='language'),
    path('country', common_views.country, name='country'),
    path('countryToState/<int:countryId>', common_views.country_to_state, name='country_to_state'),
    path('securityQuestion', common_views.security_question, name='security_question'),
    path('getRemoteAddress', common_views.get_remote_address, name='get_remote_address'),
    path('getCountrySetting/<int:countryId>/<int:planId>', common_views.get_country_setting, name='get_country_setting'),
    path('countryToStateName/<str:countryName>', common_views.country_to_state_name, name='country_to_state_name'),
    path('getCountryName/<int:countryId>', common_views.get_country_name, name='get_country_name'),
    path('getCountryId/<str:countryName>', common_views.get_country_id, name='get_country_id'),
    path('getGroupFirstRecords/<int:groupId>', common_views.get_group_first_records, name='get_group_first_records'),
    path('checkAuthorized', common_views.check_authorized, name='check_authorized'),
    path('validatePhoneFormat/<int:countryId>/<str:phoneNumber>', common_views.validate_phone_format, name='validate_phone_format'),
    path('getPriceList', common_views.get_price_list, name='get_price_list'),
]
