from django.urls import path
from affiliate_program_app.views import affiliate_program_views

urlpatterns = [
    path('affiliateProgram/getAffiliateProgramListPage', affiliate_program_views.get_affiliate_program_list_page, name='get_affiliate_program_list_page'),
    path('affiliateProgram/getAffiliateProgramById/<int:apId>', affiliate_program_views.get_affiliate_program_by_id, name='get_affiliate_program_by_id'),
    path('affiliateProgram/deleteAffiliateProgram', affiliate_program_views.delete_affiliate_program, name='delete_affiliate_program'),
    path('affiliateProgram/saveAffiliateProgram', affiliate_program_views.save_affiliate_program, name='save_affiliate_program'),
]
