import logging
import math
from typing import Any, Dict
from django.db.models import Q
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated

from auth_app.authentication import CustomJWTAuthentication
from common_app.models import CancelRegistrationLog
from common_app.responses import CustomResponse
from common_app.common_function import CommonFunction
from common_app.decrypt_string import DecryptString

logger = logging.getLogger(__name__)


def serialize_registration_log(log: CancelRegistrationLog) -> Dict[str, Any]:
    """Serializes a CancelRegistrationLog model instance to match the Java DTO contract."""
    created_date_str = None
    if log.createdDate:
        try:
            created_date_str = CommonFunction.displayDateTime(str(log.createdDate))
        except Exception:
            pass

    return {
        "id": log.id,
        "username": log.username,
        "firstName": log.firstName,
        "lastName": log.lastName,
        "email": log.email,
        "cell": log.cell,
        "step": log.step,
        "createdDate": created_date_str,
        "status": log.status
    }


@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_cancel_registrations_list_page(request: Request) -> CustomResponse:
    """
    Fetches a paginated, optionally filtered list of cancel registrations.
    Translates logic from CancelRegistrationsServiceImpl.getCancelRegistrationsListPage.
    """
    res_body: Dict[str, Any] = {}
    try:
        search_key = request.query_params.get("searchKey", "")
        page = int(request.query_params.get("page", 0))
        size = int(request.query_params.get("size", 10))

        offset = page * size
        limit = offset + size

        # Query all logs by default
        queryset = CancelRegistrationLog.objects.all().order_by('id')

        if search_key:
            # Match the Java behavior of encrypting the search term before querying
            search_key_enc = DecryptString.setEncDecUser(search_key, "", "Y")
            queryset = queryset.filter(
                Q(firstName__icontains=search_key_enc) |
                Q(lastName__icontains=search_key_enc) |
                Q(email__icontains=search_key_enc) |
                Q(username__icontains=search_key_enc)
            )

        total_records = CancelRegistrationLog.objects.count()
        filtered_count = queryset.count()
        total_pages = math.ceil(filtered_count / size) if size > 0 else 0

        paginated_logs = queryset[offset:limit]
        registration_logs_dtos = [serialize_registration_log(log) for log in paginated_logs]

        res_body["getTotalPages"] = total_pages
        res_body["getNumber"] = page
        res_body["getSize"] = size
        res_body["cancelRegistrationsList"] = registration_logs_dtos
        res_body["getTotalRecords"] = total_records

        return CustomResponse(data=res_body, status=200, message="Cancel Registrations List fetched successfully")
    except Exception as e:
        logger.error(f"get_cancel_registrations_list_page error: {e}", exc_info=True)
        return CustomResponse(data=res_body, status=500, message="error")


@api_view(['DELETE'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_cancel_registrations(request: Request) -> CustomResponse:
    """
    Deletes cancellation logs by a list of ids from the request payload.
    Translates logic from CancelRegistrationsServiceImpl.deleteCancelRegistrations.
    """
    res_body: Dict[str, Any] = {}
    try:
        ids = request.data.get("ids", [])
        for log_id in ids:
            log_exists = CancelRegistrationLog.objects.filter(id=log_id).exists()
            if log_exists:
                CancelRegistrationLog.objects.filter(id=log_id).delete()
        return CustomResponse(data=res_body, status=200, message="Cancel Registrations deleted successfully.")
    except Exception as e:
        logger.error(f"delete_cancel_registrations error: {e}", exc_info=True)
        return CustomResponse(data=res_body, status=500, message="error")
