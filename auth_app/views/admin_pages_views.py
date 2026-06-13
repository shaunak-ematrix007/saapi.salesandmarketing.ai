from typing import Any, Dict, List, Optional
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated
from auth_app.authentication import CustomJWTAuthentication
from common_app.models import AdminPage, AdminPageDetails
from common_app.responses import CustomResponse


def serialize_admin_page_dto(admin_page: Optional[AdminPage]) -> Dict[str, Any]:
    """
    Serializes AdminPage to camelCase DTO representation.
    """
    if not admin_page:
        return {}
    return {
        "pgId": admin_page.pgId,
        "pgName": admin_page.pgName,
        "pgMenuName": admin_page.pgMenuName,
        "pgModuleName": admin_page.pgModuleName
    }


def serialize_admin_page_details_dto(detail: Optional[AdminPageDetails]) -> Dict[str, Any]:
    """
    Serializes AdminPageDetails to camelCase DTO representation.
    """
    if not detail:
        return {}
    return {
        "pgdId": detail.pgdId,
        "pgdPgId": detail.pgdPgId,
        "pgdActionName": detail.pgdActionName
    }


@api_view(['POST'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def save_admin_page(request: Request) -> CustomResponse:
    """
    POST /adminPages/saveAdminPage
    Saves a new admin page or updates an existing one, and updates its details list.
    """
    res_body: Dict[str, Any] = {}
    try:
        data: Dict[str, Any] = request.data
        pg_id: Optional[int] = data.get("pgId")

        subaccount_page = None
        if pg_id is not None and pg_id > 0:
            try:
                subaccount_page = AdminPage.objects.get(pgId=pg_id)
            except AdminPage.DoesNotExist:
                pass

        if not subaccount_page:
            subaccount_page = AdminPage()

        subaccount_page.pgName = data.get("pgName")
        subaccount_page.pgMenuName = data.get("pgMenuName")
        subaccount_page.pgModuleName = data.get("pgModuleName")
        subaccount_page.save()

        # Now update details list
        action_names: List[str] = data.get("pgdCheckedActionName", [])

        # Delete existing details
        AdminPageDetails.objects.filter(pgdPgId=subaccount_page.pgId).delete()

        # Create new details
        details_list: List[AdminPageDetails] = []
        for action_name in action_names:
            detail = AdminPageDetails.objects.create(
                pgdPgId=subaccount_page.pgId,
                pgdActionName=action_name
            )
            details_list.append(detail)

        res_body["adminPage"] = serialize_admin_page_dto(subaccount_page)
        res_body["adminPageDetails"] = [serialize_admin_page_details_dto(d) for d in details_list]

    except Exception:
        return CustomResponse(data=res_body, status=500, message="Admin Save Fail")

    return CustomResponse(data=res_body, status=200, message="Admin Successfully Saved")


@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_admin_page(request: Request, pgId: int) -> CustomResponse:
    """
    GET /adminPages/getAdminPage/{pgId}
    Gets an admin page by its ID.
    """
    res_body: Dict[str, Any] = {}
    try:
        try:
            subaccount_page = AdminPage.objects.get(pgId=pgId)
            res_body["adminPage"] = serialize_admin_page_dto(subaccount_page)
        except AdminPage.DoesNotExist:
            pass
    except Exception:
        return CustomResponse(data=res_body, status=500, message="Admin Page Fetch Fail")

    return CustomResponse(data=res_body, status=200, message="Admin Page Successfully Fetched")


@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_admin_page_details(request: Request, pgId: int) -> CustomResponse:
    """
    GET /adminPages/getAdminPageDetails/{pgId}
    Gets details of an admin page by page ID, ordered by pgdId ascending.
    """
    res_body: Dict[str, Any] = {}
    try:
        details = AdminPageDetails.objects.filter(pgdPgId=pgId).order_by('pgdId')
        dtos = [serialize_admin_page_details_dto(d) for d in details]
        res_body["adminPageDetails"] = dtos
    except Exception:
        pass
    return CustomResponse(data=res_body, status=200, message="Fetch data successfully")


@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_admin_page_list(request: Request) -> CustomResponse:
    """
    GET /adminPages/getAdminPageList
    Fetches paged lists of admin pages, optionally filtered by searchKey.
    """
    res_body: Dict[str, Any] = {}
    try:
        search_key: str = request.query_params.get("searchKey", "")
        page_num: int = int(request.query_params.get("page", 0))
        size: int = int(request.query_params.get("size", 10))

        if search_key:
            pages = AdminPage.objects.filter(pgName__icontains=search_key)
        else:
            pages = AdminPage.objects.all()

        pages = pages.order_by("pgId")

        total_records = AdminPage.objects.count()
        filtered_count = pages.count()

        total_pages = (filtered_count + size - 1) // size if filtered_count > 0 else 0
        offset = page_num * size
        sliced_pages = pages[offset:offset+size]

        admin_page_dtos = [serialize_admin_page_dto(p) for p in sliced_pages]

        res_body["getTotalPages"] = total_pages
        res_body["getNumber"] = page_num
        res_body["getSize"] = size
        res_body["adminPageList"] = admin_page_dtos
        res_body["getTotalRecords"] = total_records

    except Exception:
        return CustomResponse(data=res_body, status=500, message="Admin Page List Successfully Fetched")

    return CustomResponse(data=res_body, status=200, message="Admin Page List Successfully Fetched")


@api_view(['DELETE'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_admin_page(request: Request) -> CustomResponse:
    """
    DELETE /adminPages/deleteAdminPage
    Deletes specified AdminPage records and their associated details.
    """
    res_body: Dict[str, Any] = {}
    try:
        pg_ids: List[int] = request.data.get("pgIds", [])
        for pg_id in pg_ids:
            try:
                admin_page = AdminPage.objects.get(pgId=pg_id)
                pg_id_val = admin_page.pgId
                admin_page.delete()
                AdminPageDetails.objects.filter(pgdPgId=pg_id_val).delete()
            except AdminPage.DoesNotExist:
                pass
    except Exception:
        return CustomResponse(data=res_body, status=500, message="Admin Pages Deleted Fail")

    return CustomResponse(data=res_body, status=200, message="Admin Pages Deleted Successfully")
