from typing import Any, Dict, List, Optional
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from auth_app.authentication import CustomJWTAuthentication
from common_app.models import AffiliateProgram
from common_app.responses import CustomResponse
from common_app.common_function import CommonFunction
from common_app.decrypt_string import DecryptString


def serialize_affiliate_program_dto(ap: Optional[AffiliateProgram]) -> Dict[str, Any]:
    """
    Serializes AffiliateProgram model instance to a camelCase dictionary representation.
    """
    if not ap:
        return {}

    ap_date_str: Optional[str] = None
    if ap.apDate:
        try:
            ap_date_str = CommonFunction.displayDateTime(str(ap.apDate))
        except Exception:
            try:
                ap_date_str = ap.apDate.strftime("%m/%d/%Y %H:%M:%S")
            except Exception:
                pass

    ap_expiry_date_str: Optional[str] = None
    if ap.apExpiryDate:
        try:
            ap_expiry_date_str = CommonFunction.displayDate(str(ap.apExpiryDate))
        except Exception:
            try:
                ap_expiry_date_str = ap.apExpiryDate.strftime("%m/%d/%Y")
            except Exception:
                pass

    return {
        "apId": ap.apId,
        "apTitle": ap.apTitle,
        "apCommission": float(ap.apCommission) if ap.apCommission is not None else 0.0,
        "apCommissionType": ap.apCommissionType,
        "apCode": ap.apCode,
        "apIsActive": ap.apIsActive,
        "apDate": ap_date_str,
        "apExpiryDate": ap_expiry_date_str
    }


@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_affiliate_program_list_page(request: Request) -> CustomResponse:
    """
    GET /affiliateProgram/getAffiliateProgramListPage
    Fetches paginated affiliate program list page, supporting searchKey filtering.
    """
    res_body: Dict[str, Any] = {}
    try:
        search_key: Optional[str] = request.query_params.get("searchKey")
        page_num: int = int(request.query_params.get("page", 0))
        size: int = int(request.query_params.get("size", 10))

        if search_key is None or search_key == "":
            queryset = AffiliateProgram.objects.all()
        else:
            decrypted_search = DecryptString.setEncDecUser(search_key, "", "Y")
            queryset = AffiliateProgram.objects.filter(apTitle__icontains=decrypted_search)

        # Apply sorting to guarantee consistent pagination ordering
        queryset = queryset.order_by("apId")

        total_records: int = AffiliateProgram.objects.count()
        filtered_count: int = queryset.count()

        total_pages: int = (filtered_count + size - 1) // size if filtered_count > 0 else 0
        offset: int = page_num * size
        sliced_qs = queryset[offset:offset+size]

        affiliate_program_dtos: List[Dict[str, Any]] = [
            serialize_affiliate_program_dto(ap) for ap in sliced_qs
        ]

        res_body["getTotalPages"] = total_pages
        res_body["getNumber"] = page_num
        res_body["getSize"] = size
        res_body["affiliateProgram"] = affiliate_program_dtos
        res_body["getTotalRecords"] = total_records

        return CustomResponse(data=res_body, status=200, message="Affiliate Program fetched successfully")
    except Exception:
        return CustomResponse(data=res_body, status=500, message="error")


@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_affiliate_program_by_id(request: Request, apId: int) -> CustomResponse:
    """
    GET /affiliateProgram/getAffiliateProgramById/{apId}
    Fetches details of a specific affiliate program by ID.
    """
    res_body: Dict[str, Any] = {}
    try:
        try:
            ap = AffiliateProgram.objects.get(apId=apId)
            res_body["affiliateProgram"] = serialize_affiliate_program_dto(ap)
        except AffiliateProgram.DoesNotExist:
            pass
        return CustomResponse(data=res_body, status=200, message="Affiliate Program fetched successfully")
    except Exception:
        return CustomResponse(data=res_body, status=500, message="Affiliate Program not found ")


@api_view(['DELETE'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_affiliate_program(request: Request) -> CustomResponse:
    """
    DELETE /affiliateProgram/deleteAffiliateProgram
    Deletes specified affiliate programs by IDs.
    """
    res_body: Dict[str, Any] = {}
    try:
        ap_ids: List[int] = request.data.get("apIds", [])
        for ap_id in ap_ids:
            try:
                ap = AffiliateProgram.objects.get(apId=ap_id)
                ap.delete()
            except AffiliateProgram.DoesNotExist:
                pass
        return CustomResponse(data=res_body, status=200, message="Affiliate Program deleted successfully.")
    except Exception:
        return CustomResponse(data=res_body, status=500, message="error")


@api_view(['POST'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def save_affiliate_program(request: Request) -> CustomResponse:
    """
    POST /affiliateProgram/saveAffiliateProgram
    Creates a new affiliate program or updates an existing one.
    """
    res_body: Dict[str, Any] = {}
    try:
        data: Dict[str, Any] = request.data
        ap_id: int = int(data.get("apId", 0))

        affiliate_program = None
        if ap_id and ap_id > 0:
            try:
                affiliate_program = AffiliateProgram.objects.get(apId=ap_id)
            except AffiliateProgram.DoesNotExist:
                pass

        if not affiliate_program:
            affiliate_program = AffiliateProgram()

        affiliate_program.apTitle = data.get("apTitle")
        
        commission = data.get("apCommission")
        affiliate_program.apCommission = float(commission) if commission is not None else 0.0
        
        affiliate_program.apCommissionType = data.get("apCommissionType", 1)
        affiliate_program.apCode = data.get("apCode")
        affiliate_program.apIsActive = data.get("apIsActive", "N")
        affiliate_program.apDate = timezone.now()

        ap_expiry_date = data.get("apExpiryDate")
        if ap_expiry_date:
            try:
                db_date_str = CommonFunction.dbDate(ap_expiry_date)
                affiliate_program.apExpiryDate = CommonFunction.convertDateOnly(db_date_str)
            except Exception:
                pass

        affiliate_program.save()

        if ap_id == 0:
            message = "Affiliate Program data added successfully."
        else:
            message = "Affiliate Program data updated successfully"

        return CustomResponse(data=res_body, status=200, message=message)
    except Exception:
        return CustomResponse(data=res_body, status=500, message="Error in save Affiliate Program")
