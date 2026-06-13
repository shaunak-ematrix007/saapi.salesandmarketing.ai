from typing import Any, Dict, Optional
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated
from auth_app.authentication import CustomJWTAuthentication
from common_app.models import AdminType, AdminPagePermission
from common_app.responses import CustomResponse


def serialize_admin_type_dto(admin_type: Optional[AdminType]) -> Dict[str, Any]:
    """
    Serializes AdminType model instance to camelCase DTO dictionary representation.
    """
    if not admin_type:
        return {}
    return {
        "styId": admin_type.styId,
        "styName": admin_type.styName,
        "styCreatedDate": admin_type.styCreatedDate.strftime("%m/%d/%Y") if admin_type.styCreatedDate else None
    }


@api_view(['POST'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def save_admin_user_type(request: Request) -> CustomResponse:
    """
    POST /adminType/saveAdminUserType
    Creates a new AdminType or updates an existing one, updating permissions list.
    """
    res_body: Dict[str, Any] = {}
    try:
        data: Dict[str, Any] = request.data
        sty_id: int = int(data.get("styId", 0))
        sty_name: str = data.get("styName", "")

        # Check if AdminType already exists (only for creation: styId == 0)
        exists: bool = False
        if sty_id == 0:
            exists = AdminType.objects.filter(styName=sty_name).exists()

        if not exists:
            if sty_id == 0:
                admin_type = AdminType()
                admin_type.styCreatedDate = timezone.now()
            else:
                try:
                    admin_type = AdminType.objects.get(styId=sty_id)
                except AdminType.DoesNotExist:
                    admin_type = AdminType()
                    admin_type.styCreatedDate = timezone.now()

            admin_type.styName = sty_name
            admin_type.save()

            # Delete old permissions if updating
            if sty_id > 0:
                AdminPagePermission.objects.filter(perStyId=admin_type.styId).delete()

            # Save new permissions
            pages_permissions = data.get("pages", [])
            for p in pages_permissions:
                AdminPagePermission.objects.create(
                    perPgId=p.get("perPgId"),
                    perActionName=p.get("perActionName"),
                    perStyId=admin_type.styId
                )

            if sty_id == 0:
                return CustomResponse(data=res_body, status=200, message="Add Admin account type successfully.")
            else:
                return CustomResponse(data=res_body, status=200, message="Update Admin account type successfully.")
        else:
            return CustomResponse(data=res_body, status=304, message="Admin account type already in used.")

    except Exception:
        return CustomResponse(data=res_body, status=500, message="error")


@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_admin_user_type(request: Request, id: int) -> CustomResponse:
    """
    GET /adminType/getAdminUserType/{id}
    Fetches details of a specific AdminType by ID.
    """
    res_body: Dict[str, Any] = {}
    try:
        try:
            admin_type = AdminType.objects.get(styId=id)
            res_body["adminUserType"] = serialize_admin_type_dto(admin_type)
        except AdminType.DoesNotExist:
            pass
    except Exception:
        return CustomResponse(data=res_body, status=500, message="Admin User Type Fetch Fail")

    return CustomResponse(data=res_body, status=200, message="Admin User Type Successfully Fetched")


@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_admin_user_type_list_page(request: Request) -> CustomResponse:
    """
    GET /adminType/getAdminUserTypeListPage
    Fetches paged lists of AdminType roles, supporting searchKey filtering.
    """
    res_body: Dict[str, Any] = {}
    try:
        search_key: str = request.query_params.get("searchKey", "")
        page_num: int = int(request.query_params.get("page", 0))
        size: int = int(request.query_params.get("size", 10))

        if search_key:
            admin_types = AdminType.objects.filter(styName__icontains=search_key)
        else:
            admin_types = AdminType.objects.all()

        admin_types = admin_types.order_by("styId")

        total_records: int = AdminType.objects.count()
        filtered_count: int = admin_types.count()

        total_pages: int = (filtered_count + size - 1) // size if filtered_count > 0 else 0
        offset: int = page_num * size
        sliced_types = admin_types[offset:offset+size]

        dtos = [serialize_admin_type_dto(t) for t in sliced_types]

        res_body["getTotalPages"] = total_pages
        res_body["getNumber"] = page_num
        res_body["getSize"] = size
        res_body["adminUserTypeListPage"] = dtos
        res_body["getTotalRecords"] = total_records

    except Exception:
        return CustomResponse(data=res_body, status=200, message="Admin User Type List Fetch Fail")

    return CustomResponse(data=res_body, status=200, message="Admin User Type List Fetched Successfully")


@api_view(['DELETE'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_admin_user_type(request: Request) -> CustomResponse:
    """
    DELETE /adminType/deleteAdminUserType
    Deletes specified AdminType roles by IDs.
    """
    res_body: Dict[str, Any] = {}
    try:
        data: Dict[str, Any] = request.data
        ids_list = data.get("ids") or data.get("Ids") or []
        for sty_id in ids_list:
            try:
                admin_type = AdminType.objects.get(styId=sty_id)
                admin_type.delete()
            except AdminType.DoesNotExist:
                pass
    except Exception:
        return CustomResponse(data=res_body, status=500, message="error")

    return CustomResponse(data=res_body, status=200, message="Admin User Type deleted successfully.")
