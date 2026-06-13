# Reminder: Register 'generalsections_app' in INSTALLED_APPS inside settings.py
import logging
import math
from typing import Any, Dict, Optional
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated

from auth_app.authentication import CustomJWTAuthentication
from common_app.models import PlanModule
from common_app.responses import CustomResponse

logger = logging.getLogger(__name__)


def to_int(val: Any) -> Optional[int]:
    if val is None or val == "":
        return None
    try:
        return int(val)
    except (ValueError, TypeError):
        return None


def serialize_plan_module(pm: PlanModule) -> Dict[str, Any]:
    """Serializes a PlanModule to a dictionary."""
    return {
        "pmId": pm.pmId,
        "pmTitle": pm.pmTitle
    }


@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_plan_module(request: Request, pmId: int) -> CustomResponse:
    """Fetches plan module details by ID."""
    res_body: Dict[str, Any] = {}
    try:
        pm = PlanModule.objects.filter(pmId=pmId).first()
        if pm:
            res_body["planModule"] = serialize_plan_module(pm)
        else:
            res_body["planModule"] = None
        return CustomResponse(data=res_body, status=200, message="Plan Module fetched successfully.")
    except Exception as e:
        logger.error(f"get_plan_module error: {e}", exc_info=True)
        return CustomResponse(data=res_body, status=500, message="error")


@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_plan_module_list(request: Request) -> CustomResponse:
    """Lists all plan modules sorted by pmId."""
    res_body: Dict[str, Any] = {}
    try:
        pm_list = PlanModule.objects.all().order_by('pmId')
        dtos = [serialize_plan_module(pm) for pm in pm_list]
        res_body["planModuleList"] = dtos
        return CustomResponse(data=res_body, status=200, message="Plan Module list fetched successfully.")
    except Exception as e:
        logger.error(f"get_plan_module_list error: {e}", exc_info=True)
        return CustomResponse(data=res_body, status=500, message="error")


@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_plan_module_page_list(request: Request) -> CustomResponse:
    """Lists plan modules with pagination and search by title."""
    res_body: Dict[str, Any] = {}
    try:
        search_key = request.query_params.get("searchKey", "")
        page = int(request.query_params.get("page", 0))
        size = int(request.query_params.get("size", 10))

        offset = page * size
        limit = offset + size

        base_query = PlanModule.objects.all().order_by('pmId')
        if search_key:
            base_query = base_query.filter(pmTitle__icontains=search_key)

        total_records = PlanModule.objects.count()
        filtered_count = base_query.count()
        total_pages = math.ceil(filtered_count / size) if size > 0 else 0

        paginated_list = base_query[offset:limit]
        dtos = [serialize_plan_module(pm) for pm in paginated_list]

        res_body["getTotalPages"] = total_pages
        res_body["getNumber"] = page
        res_body["getSize"] = size
        res_body["getTotalRecords"] = total_records
        res_body["planModuleList"] = dtos

        return CustomResponse(data=res_body, status=200, message="Plan Module list fetched successfully.")
    except Exception as e:
        logger.error(f"get_plan_module_page_list error: {e}", exc_info=True)
        return CustomResponse(data=res_body, status=500, message="error")


@api_view(['POST'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def save_plan_module(request: Request) -> CustomResponse:
    """Saves or updates a plan module configuration."""
    res_body: Dict[str, Any] = {"error": ""}
    try:
        pm_id = to_int(request.data.get("pmId")) or 0
        pm_title = request.data.get("pmTitle")

        check_plan_module = None
        if pm_id == 0:
            check_plan_module = PlanModule.objects.filter(pmTitle=pm_title).first()
        else:
            check_plan_module = PlanModule.objects.filter(pmTitle=pm_title).exclude(pmId=pm_id).first()

        if check_plan_module is None:
            if pm_id > 0:
                pm = PlanModule.objects.filter(pmId=pm_id).first()
                if not pm:
                    pm = PlanModule(pmId=pm_id)
            else:
                pm = PlanModule()

            pm.pmTitle = pm_title
            pm.save()

            return CustomResponse(data=res_body, status=200, message="Save Plan Module successfully.")
        else:
            res_body["error"] = "Plan Module name already exists"
            return CustomResponse(data=res_body, status=500, message=res_body["error"])

    except Exception as e:
        logger.error(f"save_plan_module error: {e}", exc_info=True)
        res_body["error"] = "error"
        return CustomResponse(data=res_body, status=500, message="error")


@api_view(['DELETE'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_plan_module(request: Request) -> CustomResponse:
    """Bulk deletes plan modules by their IDs."""
    res_body: Dict[str, Any] = {}
    try:
        pm_ids = request.data.get("pmIds", [])
        if pm_ids:
            PlanModule.objects.filter(pmId__in=pm_ids).delete()
        return CustomResponse(data=res_body, status=200, message="Plan Module deleted successfully.")
    except Exception as e:
        logger.error(f"delete_plan_module error: {e}", exc_info=True)
        return CustomResponse(data=res_body, status=500, message="error")
