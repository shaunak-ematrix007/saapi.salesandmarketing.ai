from django.urls import path
from freetemplate_app.views import free_template_views

urlpatterns = [
    path('freeTemplate/getFreeTemplateList/<int:mpStageId>', free_template_views.get_free_template_list, name='get_free_template_list'),
]
