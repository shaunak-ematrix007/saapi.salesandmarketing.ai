from typing import Any, Dict, List, Optional
import logging

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated

from auth_app.authentication import CustomJWTAuthentication
from common_app.models import SubaccountPage, SubaccountPageDetails
from common_app.responses import CustomResponse

logger = logging.getLogger(__name__)


def serialize_subaccount_page_dto(page: Optional[SubaccountPage]) -> Dict[str, Any]:
    """
    Serializes a SubaccountPage instance to the camelCase SubaccountPageDto structure.
    """
    if not page:
        return {}
    return {
        "pgId": page.pgId,
        "pgName": page.pgName,
        "pgMenuName": page.pgMenuName,
        "pgModuleName": page.pgModuleName
    }


def serialize_subaccount_page_details_dto(details: Optional[SubaccountPageDetails]) -> Dict[str, Any]:
    """
    Serializes a SubaccountPageDetails instance to the camelCase SubaccountPageDetailsDto structure.
    """
    if not details:
        return {}
    return {
        "pgdId": details.pgdId,
        "pgdPgId": details.pgdPgId,
        "pgdActionName": details.pgdActionName
    }


@api_view(['POST'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def save_subaccount_page(request: Request) -> CustomResponse:
    """
    POST /subaccountPages/saveSubaccountPage
    Creates or updates a subaccount page along with its check-marked action names.
    """
    res_body: Dict[str, Any] = {}
    try:
        data: Dict[str, Any] = request.data
        pg_id: Optional[int] = data.get("pgId")

        subaccount_page = None
        if pg_id is not None:
            try:
                subaccount_page = SubaccountPage.objects.get(pgId=pg_id)
            except SubaccountPage.DoesNotExist:
                pass

        if subaccount_page is not None:
            # Existing page: as per Java logic, attributes are NOT modified or saved
            pass
        else:
            # New page
            subaccount_page = SubaccountPage()
            subaccount_page.pgName = data.get("pgName")
            subaccount_page.pgMenuName = data.get("pgMenuName")
            subaccount_page.pgModuleName = data.get("pgModuleName")
            subaccount_page.save()

        # Delete existing permissions for this page
        try:
            SubaccountPageDetails.objects.filter(pgdPgId=subaccount_page.pgId).delete()
        except Exception as e:
            logger.error(f"delete if PgId is available when edit {str(e)}")

        subaccount_page_details_list: List[SubaccountPageDetails] = []
        pgd_checked_action_names: List[str] = data.get("pgdCheckedActionName", [])
        for action_name in pgd_checked_action_names:
            detail = SubaccountPageDetails(
                pgdPgId=subaccount_page.pgId,
                pgdActionName=action_name
            )
            detail.save()
            subaccount_page_details_list.append(detail)

        res_body["subaccountPage"] = serialize_subaccount_page_dto(subaccount_page)
        res_body["subaccountPageDetails"] = [
            serialize_subaccount_page_details_dto(d) for d in subaccount_page_details_list
        ]
        return CustomResponse(data=res_body, status=200, message="Sub Account Type Permission Successfully Saved")
    except Exception as ex:
        logger.error(f"saveSubaccountPage error: {str(ex)}")
        return CustomResponse(data=res_body, status=500, message="Sub Account Type Permission Save Fail")


@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_subaccount_page(request: Request, pgId: int) -> CustomResponse:
    """
    GET /subaccountPages/getSubaccountPage/{pgId}
    Retrieves subaccount page details and its page permission list.
    """
    res_body: Dict[str, Any] = {}
    try:
        try:
            subaccount_page = SubaccountPage.objects.get(pgId=pgId)
            res_body["subaccountPage"] = serialize_subaccount_page_dto(subaccount_page)

            page_permission_list = list(
                SubaccountPageDetails.objects.filter(pgdPgId=pgId)
                .values_list('pgdActionName', flat=True)
            )
            res_body["subaccountPagePermissionList"] = page_permission_list
        except SubaccountPage.DoesNotExist:
            pass
        return CustomResponse(data=res_body, status=200, message="Sub Account Type Permission Successfully Fetched")
    except Exception as ex:
        logger.error(f"getSubaccountPage error: {str(ex)}")
        return CustomResponse(data=res_body, status=500, message="Sub Account Type Permission Fetch Fail")


@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_subaccount_page_details(request: Request, pgId: int) -> CustomResponse:
    """
    GET /subaccountPages/getSubaccountPageDetails/{pgId}
    Retrieves the list of permission details associated with a subaccount page.
    """
    res_body: Dict[str, Any] = {}
    try:
        details = SubaccountPageDetails.objects.filter(pgdPgId=pgId).order_by('pgdId')
        dtos = [serialize_subaccount_page_details_dto(d) for d in details]
        res_body["subaccountPageDetails"] = dtos
        return CustomResponse(data=res_body, status=200, message="Fetch data successfully")
    except Exception as ex:
        logger.error(f"getSubaccountPageDetails error: {str(ex)}")
        return CustomResponse(data=res_body, status=500, message="error")


@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_subaccount_page_list(request: Request) -> CustomResponse:
    """
    GET /subaccountPages/getSubaccountPageList
    Fetches paginated list of subaccount pages with optional searchKey filtering.
    """
    res_body: Dict[str, Any] = {}
    try:
        search_key: Optional[str] = request.query_params.get("searchKey")

        try:
            page_num = int(request.query_params.get("page", 0))
            if page_num < 0:
                page_num = 0
        except (TypeError, ValueError):
            page_num = 0

        try:
            size = int(request.query_params.get("size", 10))
            if size <= 0:
                size = 10
        except (TypeError, ValueError):
            size = 10

        if search_key is None or search_key == "":
            queryset = SubaccountPage.objects.all()
        else:
            queryset = SubaccountPage.objects.filter(pgName__icontains=search_key)

        queryset = queryset.order_by("pgId")
        total_records = queryset.count()

        total_pages = (total_records + size - 1) // size if total_records > 0 else 0
        offset = page_num * size
        sliced_qs = queryset[offset:offset + size]

        subaccount_page_dtos = [serialize_subaccount_page_dto(p) for p in sliced_qs]

        res_body["getTotalPages"] = total_pages
        res_body["getNumber"] = page_num
        res_body["getSize"] = size
        res_body["subaccountPageList"] = subaccount_page_dtos
        res_body["getTotalRecords"] = SubaccountPage.objects.count()

        return CustomResponse(data=res_body, status=200, message="Sub Account Type Permission List Successfully Fetched")
    except Exception as ex:
        logger.error(f"getSubaccountPageList error: {str(ex)}")
        return CustomResponse(data=res_body, status=500, message="Sub Account Type Permission List Successfully Fetched")


@api_view(['DELETE'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_subaccount_page(request: Request) -> CustomResponse:
    """
    DELETE /subaccountPages/deleteSubaccountPage
    Deletes subaccount pages by their IDs.
    """
    res_body: Dict[str, Any] = {}
    try:
        pg_ids: List[int] = request.data.get("pgIds", [])
        for pg_id in pg_ids:
            try:
                subaccount_page = SubaccountPage.objects.get(pgId=pg_id)
                subaccount_page.delete()
            except SubaccountPage.DoesNotExist:
                pass
        return CustomResponse(data=res_body, status=200, message="Sub Account Type Permission Deleted Successfully")
    except Exception as ex:
        logger.error(f"deleteSubaccountPage error: {str(ex)}")
        return CustomResponse(data=res_body, status=500, message="Sub Account Type Permission Deleted Fail")
