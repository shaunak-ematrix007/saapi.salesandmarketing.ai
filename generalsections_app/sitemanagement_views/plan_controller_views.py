import logging
import math
from typing import Any, Dict, Optional
from django.utils import timezone
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated

from auth_app.authentication import CustomJWTAuthentication
from common_app.models import Plan, CountrySetting
from common_app.responses import CustomResponse
from generalsections_app.sitemanagement_views.country_settings_views import serialize_country_settings_detail

logger = logging.getLogger(__name__)


def to_int(val: Any) -> Optional[int]:
    if val is None or val == "":
        return None
    try:
        return int(val)
    except (ValueError, TypeError):
        return None


def serialize_plan(plan: Plan, country_setting: Optional[CountrySetting] = None) -> Dict[str, Any]:
    """Serializes a Plan to a dictionary, including embedded country settings if provided."""
    return {
        "planId": plan.planId,
        "planName": plan.planName,
        "planActive": plan.planActive,
        "planVisibility": plan.planVisibility,
        "planPmIdList": plan.planPmIdList,
        "countrySetting": serialize_country_settings_detail(country_setting) if country_setting else None
    }


@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_plan_by_id(request: Request, countryId: int, planId: int) -> CustomResponse:
    """Fetches details of a plan including country-specific configurations."""
    res_body: Dict[str, Any] = {}
    try:
        plan = Plan.objects.filter(planId=planId).first()
        if plan:
            cs = CountrySetting.objects.filter(cntyId=countryId, cntyPlanId=planId).first()
            res_body["plan"] = serialize_plan(plan, cs)
        else:
            res_body["plan"] = None
        return CustomResponse(data=res_body, status=200, message="Plan fetched successfully.")
    except Exception as e:
        logger.error(f"get_plan_by_id error: {e}", exc_info=True)
        return CustomResponse(data=res_body, status=500, message="error")


@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_plan_list_by_id(request: Request, countryId: int) -> CustomResponse:
    """Lists plans for a specific country."""
    res_body: Dict[str, Any] = {}
    try:
        plan_dtos = []
        country_setting_list = CountrySetting.objects.filter(cntyId=countryId)
        for cs in country_setting_list:
            plan = Plan.objects.filter(planId=cs.cntyPlanId).first()
            if plan:
                plan_dtos.append(serialize_plan(plan, cs))
        res_body["planList"] = plan_dtos
        return CustomResponse(data=res_body, status=200, message="Plan list fetched successfully.")
    except Exception as e:
        logger.error(f"get_plan_list_by_id error: {e}", exc_info=True)
        return CustomResponse(data=res_body, status=500, message="error")


@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_plan(request: Request, planId: int) -> CustomResponse:
    """Fetches plan details by planId."""
    res_body: Dict[str, Any] = {}
    try:
        plan = Plan.objects.filter(planId=planId).first()
        if plan:
            res_body["plan"] = serialize_plan(plan)
        else:
            res_body["plan"] = None
        return CustomResponse(data=res_body, status=200, message="Plan fetched successfully.")
    except Exception as e:
        logger.error(f"get_plan error: {e}", exc_info=True)
        return CustomResponse(data=res_body, status=500, message="error")


@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_plan_list(request: Request) -> CustomResponse:
    """Lists plans with search functionality and pagination."""
    res_body: Dict[str, Any] = {}
    try:
        search_key = request.query_params.get("searchKey", "")
        page = int(request.query_params.get("page", 0))
        size = int(request.query_params.get("size", 10))

        offset = page * size
        limit = offset + size

        base_query = Plan.objects.all().order_by('planId')
        if search_key:
            base_query = base_query.filter(planName__icontains=search_key)

        total_records = Plan.objects.count()
        filtered_count = base_query.count()
        total_pages = math.ceil(filtered_count / size) if size > 0 else 0

        paginated_plans = base_query[offset:limit]
        plan_dtos = [serialize_plan(p) for p in paginated_plans]

        res_body["getTotalPages"] = total_pages
        res_body["getNumber"] = page
        res_body["getSize"] = size
        res_body["getTotalRecords"] = total_records
        res_body["planList"] = plan_dtos

        return CustomResponse(data=res_body, status=200, message="Plan list fetched successfully.")
    except Exception as e:
        logger.error(f"get_plan_list error: {e}", exc_info=True)
        return CustomResponse(data=res_body, status=500, message="error")


@api_view(['POST'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def save_plan(request: Request) -> CustomResponse:
    """Saves or updates a plan configuration."""
    res_body: Dict[str, Any] = {"error": ""}
    try:
        plan_id = to_int(request.data.get("planId")) or 0
        plan_name = request.data.get("planName")
        plan_visibility = request.data.get("planVisibility", "Public")
        plan_active = request.data.get("planActive", "Y")
        plan_pm_id_list = request.data.get("planPmIdList")

        check_plan = None
        if plan_id == 0:
            check_plan = Plan.objects.filter(planName=plan_name).first()
        else:
            check_plan = Plan.objects.filter(planName=plan_name).exclude(planId=plan_id).first()

        if check_plan is None:
            if plan_id > 0:
                plan = Plan.objects.filter(planId=plan_id).first()
                if not plan:
                    plan = Plan(planId=plan_id)
            else:
                plan = Plan()
                plan.planAddedDate = timezone.now()

            plan.planName = plan_name
            plan.planVisibility = plan_visibility
            plan.planActive = plan_active
            plan.planPmIdList = plan_pm_id_list
            plan.save()

            return CustomResponse(data=res_body, status=200, message="Save plan successfully.")
        else:
            res_body["error"] = "Plan name already exists"
            return CustomResponse(data=res_body, status=500, message=res_body["error"])
    except Exception as e:
        logger.error(f"save_plan error: {e}", exc_info=True)
        res_body["error"] = "error"
        return CustomResponse(data=res_body, status=500, message="error")


@api_view(['DELETE'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_plan(request: Request) -> CustomResponse:
    """Soft-deletes plans by setting planActive to 'N'."""
    res_body: Dict[str, Any] = {}
    try:
        plan_ids = request.data.get("planIds", [])
        if plan_ids:
            Plan.objects.filter(planId__in=plan_ids).update(planActive="N")
        return CustomResponse(data=res_body, status=200, message="Plan deleted successfully.")
    except Exception as e:
        logger.error(f"delete_plan error: {e}", exc_info=True)
        return CustomResponse(data=res_body, status=500, message="error")


@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_plan_list_combo(request: Request) -> CustomResponse:
    """Fetches plan list combo sorted by planId."""
    res_body: Dict[str, Any] = {}
    try:
        plans = Plan.objects.all().order_by('planId')
        plan_dtos = [serialize_plan(p) for p in plans]
        res_body["planList"] = plan_dtos
        return CustomResponse(data=res_body, status=200, message="Plan list fetched successfully.")
    except Exception as e:
        logger.error(f"get_plan_list_combo error: {e}", exc_info=True)
        return CustomResponse(data=res_body, status=500, message="error")
