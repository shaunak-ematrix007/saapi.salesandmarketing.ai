import logging
import math
from typing import Any, Dict, Optional
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated

from auth_app.authentication import CustomJWTAuthentication
from common_app.models import EmailVerificationPrice
from common_app.responses import CustomResponse

logger = logging.getLogger(__name__)


def to_float(val: Any) -> float:
    if val is None or val == "":
        return 0.0
    try:
        return float(val)
    except (ValueError, TypeError):
        return 0.0


def to_int(val: Any) -> Optional[int]:
    if val is None or val == "":
        return None
    try:
        return int(val)
    except (ValueError, TypeError):
        return None


def serialize_evp(evp: EmailVerificationPrice) -> Dict[str, Any]:
    """Serializes EmailVerificationPrice to dictionary."""
    return {
        "evpId": evp.evpId,
        "evpContactTotal": evp.evpContactTotal,
        "evpRate": evp.evpRate,
        "evpCntyId": evp.evpCntyId,
    }


@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_email_verification_price_list(request: Request) -> CustomResponse:
    """Lists email verification pricing tiers with search & pagination."""
    res_body: Dict[str, Any] = {}
    try:
        search_key = request.query_params.get("searchKey", "")
        page = int(request.query_params.get("page", 0))
        size = int(request.query_params.get("size", 10))

        offset = page * size
        limit = offset + size

        base_query = EmailVerificationPrice.objects.all().order_by('evpId')
        if search_key:
            base_query = base_query.filter(evpContactTotal__icontains=search_key)

        total_records = EmailVerificationPrice.objects.count()
        filtered_count = base_query.count()
        total_pages = math.ceil(filtered_count / size) if size > 0 else 0

        paginated_list = base_query[offset:limit]
        dtos = [serialize_evp(ev) for ev in paginated_list]

        res_body["getTotalPages"] = total_pages
        res_body["getNumber"] = page
        res_body["getSize"] = size
        res_body["getTotalRecords"] = total_records
        res_body["emailVerificationList"] = dtos

        return CustomResponse(data=res_body, status=200, message="Email verification price list fetched successfully.")
    except Exception as e:
        logger.error(f"get_email_verification_price_list error: {e}", exc_info=True)
        return CustomResponse(data=res_body, status=500, message="error")


@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_email_verification_price_list_by_country_id(request: Request, countryId: int) -> CustomResponse:
    """Lists email verification price list filtered by countryId."""
    res_body: Dict[str, Any] = {}
    try:
        ev_list = EmailVerificationPrice.objects.filter(evpCntyId=countryId).order_by('evpContactTotal')
        dtos = [serialize_evp(ev) for ev in ev_list]
        res_body["emailVerificationList"] = dtos
        return CustomResponse(data=res_body, status=200, message="Email verification price list fetched successfully.")
    except Exception as e:
        logger.error(f"get_email_verification_price_list_by_country_id error: {e}", exc_info=True)
        return CustomResponse(data=res_body, status=500, message="error")


@api_view(['POST'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def save_email_verification_price(request: Request) -> CustomResponse:
    """Creates or updates an email verification pricing tier."""
    res_body: Dict[str, Any] = {"error": ""}
    try:
        evp_id = to_int(request.data.get("evpId")) or 0
        evp_contact_total = to_int(request.data.get("evpContactTotal"))
        evp_rate = to_float(request.data.get("evpRate"))
        evp_cnty_id = to_int(request.data.get("evpCntyId"))

        check_price = None
        if evp_id == 0:
            check_price = EmailVerificationPrice.objects.filter(
                evpContactTotal=evp_contact_total, evpCntyId=evp_cnty_id
            ).first()
        else:
            check_price = EmailVerificationPrice.objects.filter(
                evpContactTotal=evp_contact_total, evpCntyId=evp_cnty_id
            ).exclude(evpId=evp_id).first()

        if check_price is None:
            if evp_id > 0:
                evp = EmailVerificationPrice.objects.filter(evpId=evp_id, evpCntyId=evp_cnty_id).first()
                if not evp:
                    evp = EmailVerificationPrice(evpId=evp_id)
            else:
                evp = EmailVerificationPrice()

            evp.evpContactTotal = evp_contact_total
            evp.evpRate = evp_rate
            evp.evpCntyId = evp_cnty_id
            evp.save()

            return CustomResponse(data=res_body, status=200, message="Save email verification price successfully.")
        else:
            res_body["error"] = "Email verification price already exists"
            return CustomResponse(data=res_body, status=500, message=res_body["error"])

    except Exception as e:
        logger.error(f"save_email_verification_price error: {e}", exc_info=True)
        res_body["error"] = "error"
        return CustomResponse(data=res_body, status=500, message="error")


@api_view(['DELETE'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_email_verification_price(request: Request) -> CustomResponse:
    """Bulk deletes email verification prices."""
    res_body: Dict[str, Any] = {}
    try:
        evp_ids = request.data.get("evpIds", [])
        if evp_ids:
            EmailVerificationPrice.objects.filter(evpId__in=evp_ids).delete()
        return CustomResponse(data=res_body, status=200, message="Email verification price deleted successfully.")
    except Exception as e:
        logger.error(f"delete_email_verification_price error: {e}", exc_info=True)
        return CustomResponse(data=res_body, status=500, message="error")


@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_email_verification_price(request: Request, evpId: int) -> CustomResponse:
    """Fetches details of a specific pricing tier by ID."""
    res_body: Dict[str, Any] = {}
    try:
        ev = EmailVerificationPrice.objects.filter(evpId=evpId).first()
        if ev:
            res_body["emailVerificationPrice"] = serialize_evp(ev)
        else:
            res_body["emailVerificationPrice"] = None
        return CustomResponse(data=res_body, status=200, message="Email verification price fetched successfully.")
    except Exception as e:
        logger.error(f"get_email_verification_price error: {e}", exc_info=True)
        return CustomResponse(data=res_body, status=500, message="error")
