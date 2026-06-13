import logging
from typing import Any, Dict

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated

from auth_app.authentication import CustomJWTAuthentication
from common_app.models import Settings as SiteSettings
from common_app.responses import CustomResponse

logger = logging.getLogger(__name__)


@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_site_settings(request: Request) -> CustomResponse:
    """Retrieves the global site settings config."""
    res_body: Dict[str, Any] = {}
    try:
        settings = SiteSettings.objects.first()
        if settings:
            dto = {
                "id": settings.id,
                "adminName": settings.adminName,
                "adminEmail": settings.adminEmail,
                "facebookLink": settings.facebookLink,
                "twitterLink": settings.twitterLink,
                "gplusLink": settings.gplusLink,
                "linkinLink": settings.linkinLink,
                "siteOnOff": settings.siteOnOff,
                "logoName": settings.logoName,
                "logoSystemName": settings.logoSystemName,
                "paymentSwitch": settings.paymentSwitch,
                "billPeriod": settings.billPeriod,
                "assessmentPrice": settings.assessmentPrice,
                "surveyPrice": settings.surveyPrice,
                "individualPrice": settings.individualPrice
            }
            # Clean None/null fields to mimic Java's @JsonInclude(NON_NULL)
            dto = {k: v for k, v in dto.items() if v is not None}
            res_body["siteSettings"] = dto
        else:
            res_body["siteSettings"] = None

        return CustomResponse(data=res_body, status=200, message="getSiteSettings")
    except Exception as e:
        logger.error(f"getSiteSettings error: {e}", exc_info=True)
        return CustomResponse(data=res_body, status=500, message="error")


@api_view(['POST'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def update_site_settings(request: Request) -> CustomResponse:
    """Updates the site settings config, returning the state prior to update."""
    res_body: Dict[str, Any] = {}
    try:
        dto_id = request.data.get("id")
        settings = SiteSettings.objects.filter(id=dto_id).first()

        # Update or create the settings entity
        updated_settings = SiteSettings(
            id=dto_id,
            adminName=request.data.get("adminName"),
            adminEmail=request.data.get("adminEmail"),
            facebookLink=request.data.get("facebookLink"),
            twitterLink=request.data.get("twitterLink"),
            gplusLink=request.data.get("gplusLink"),
            linkinLink=request.data.get("linkinLink"),
            siteOnOff=request.data.get("siteOnOff"),
            logoName=request.data.get("logoName"),
            logoSystemName=request.data.get("logoSystemName"),
            paymentSwitch=request.data.get("paymentSwitch"),
            billPeriod=request.data.get("billPeriod"),
            assessmentPrice=float(request.data.get("assessmentPrice", 0.0)),
            surveyPrice=float(request.data.get("surveyPrice", 0.0)),
            individualPrice=float(request.data.get("individualPrice", 0.0))
        )
        updated_settings.save()

        # Replicate Java behavior where the old entity state is returned
        if settings:
            old_dto = {
                "id": settings.id,
                "adminName": settings.adminName,
                "adminEmail": settings.adminEmail,
                "facebookLink": settings.facebookLink,
                "twitterLink": settings.twitterLink,
                "gplusLink": settings.gplusLink,
                "linkinLink": settings.linkinLink,
                "siteOnOff": settings.siteOnOff,
                "logoName": settings.logoName,
                "logoSystemName": settings.logoSystemName,
                "paymentSwitch": settings.paymentSwitch,
                "billPeriod": settings.billPeriod,
                "assessmentPrice": settings.assessmentPrice,
                "surveyPrice": settings.surveyPrice,
                "individualPrice": settings.individualPrice
            }
            old_dto = {k: v for k, v in old_dto.items() if v is not None}
            res_body["updateSiteSettings"] = old_dto
        else:
            res_body["updateSiteSettings"] = None

        return CustomResponse(data=res_body, status=200, message="site settings successfully updated")
    except Exception as e:
        logger.error(f"updateSiteSettings error: {e}", exc_info=True)
        return CustomResponse(data=res_body, status=500, message="error")
