import logging
import math
from typing import Any, Dict
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated

from auth_app.authentication import CustomJWTAuthentication
from common_app.models import MonthlyPrice
from common_app.responses import CustomResponse

logger = logging.getLogger(__name__)


@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_monthly_price_by_id(request: Request, monthlyPriceId: int) -> CustomResponse:
    """
    Fetches monthly price details by ID.
    Translates logic from MonthlyPriceServicesImpl.getMonthlyPriceById.
    """
    res_body: Dict[str, Any] = {}
    try:
        # Match Java: findMonthlyPriceBymnpId
        monthly_price = MonthlyPrice.objects.filter(mnpId=monthlyPriceId).first()
        if monthly_price:
            res_body["MonthlyPrice"] = {
                "mnpId": monthly_price.mnpId,
                "mnpType": monthly_price.mnpType,
                "mnpQty": monthly_price.mnpQty,
                "mnpPrice": monthly_price.mnpPrice,
                "mnpCountryId": monthly_price.mnpCountryId
            }
        else:
            res_body["MonthlyPrice"] = None
        return CustomResponse(data=res_body, status=200, message="Monthly Price Fetched Successfully")
    except Exception as e:
        logger.error(f"get_monthly_price_by_id error: {e}", exc_info=True)
        return CustomResponse(data=res_body, status=500, message="Monthly Price Fetched Fail")


@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_monthly_price_list_page(request: Request) -> CustomResponse:
    """
    Returns a paginated list of monthly prices, optionally filtered by type.
    Translates logic from MonthlyPriceServicesImpl.getMonthlyPriceListPage.
    """
    res_body: Dict[str, Any] = {}
    try:
        search_key = request.query_params.get("searchKey", "")
        page = int(request.query_params.get("page", 0))
        size = int(request.query_params.get("size", 10))

        offset = page * size
        limit = offset + size

        queryset = MonthlyPrice.objects.all().order_by('mnpId')

        if search_key:
            # Match Java: Select mp from MonthlyPrice mp where lower(mp.mnpType) like lower(CONCAT('%', :searchKey, '%'))
            queryset = queryset.filter(mnpType__icontains=search_key)

        total_records = MonthlyPrice.objects.count()
        filtered_count = queryset.count()
        total_pages = math.ceil(filtered_count / size) if size > 0 else 0

        paginated_prices = queryset[offset:limit]
        
        monthly_price_dtos = []
        for mp in paginated_prices:
            monthly_price_dtos.append({
                "mnpId": mp.mnpId,
                "mnpType": mp.mnpType,
                "mnpQty": mp.mnpQty,
                "mnpPrice": mp.mnpPrice,
                "mnpCountryId": mp.mnpCountryId
            })

        res_body["getTotalPages"] = total_pages
        res_body["getNumber"] = page
        res_body["getSize"] = size
        res_body["monthlyPriceListPage"] = monthly_price_dtos
        res_body["getTotalRecords"] = total_records

        return CustomResponse(data=res_body, status=200, message="Monthly Price Successfully")
    except Exception as e:
        logger.error(f"get_monthly_price_list_page error: {e}", exc_info=True)
        return CustomResponse(data=res_body, status=500, message="error")


@api_view(['POST'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def save_monthly_price(request: Request) -> CustomResponse:
    """
    Saves or updates monthly price properties.
    Translates logic from MonthlyPriceServicesImpl.saveMonthlyPrice.
    """
    res_body: Dict[str, Any] = {}
    try:
        monthly_price_dto = request.data
        mnp_id = monthly_price_dto.get("mnpId")
        if mnp_id:
            # In Java: save() will update if ID exists, insert if not.
            monthly_price = MonthlyPrice.objects.filter(mnpId=mnp_id).first()
            if not monthly_price:
                monthly_price = MonthlyPrice(mnpId=mnp_id)
        else:
            monthly_price = MonthlyPrice()

        monthly_price.mnpType = monthly_price_dto.get("mnpType")
        
        # Convert qty to int if present, or leave None
        mnp_qty = monthly_price_dto.get("mnpQty")
        if mnp_qty is not None:
            monthly_price.mnpQty = int(mnp_qty)
        else:
            monthly_price.mnpQty = None

        # Convert price to float if present, or leave None
        mnp_price = monthly_price_dto.get("mnpPrice")
        if mnp_price is not None:
            monthly_price.mnpPrice = float(mnp_price)
        else:
            monthly_price.mnpPrice = None

        # Convert country ID to int if present, or leave None
        mnp_country_id = monthly_price_dto.get("mnpCountryId")
        if mnp_country_id is not None:
            monthly_price.mnpCountryId = int(mnp_country_id)
        else:
            monthly_price.mnpCountryId = None

        monthly_price.save()

        res_body["msg"] = "Monthly Price Saved Successfully"
        return CustomResponse(data=res_body, status=200, message="Monthly Price Saved Successfully")
    except Exception as e:
        logger.error(f"save_monthly_price error: {e}", exc_info=True)
        # Note: Java returns status 200 (HttpStatus.OK) even on exception for Save Fail
        return CustomResponse(data=res_body, status=200, message="Monthly Price Save Fail")


@api_view(['DELETE'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_monthly_price(request: Request) -> CustomResponse:
    """
    Bulk deletes monthly prices by their IDs.
    Translates logic from MonthlyPriceServicesImpl.deleteMonthlyPrice.
    """
    res_body: Dict[str, Any] = {}
    try:
        delete_monthly_price_dto = request.data
        mnp_ids = delete_monthly_price_dto.get("mnpIds", [])
        for mnp_id in mnp_ids:
            # In Java: findById(Id).isPresent() then deleteById(Id)
            MonthlyPrice.objects.filter(mnpId=mnp_id).delete()
        return CustomResponse(data=res_body, status=200, message="Monthly Price Deleted Successfully")
    except Exception as e:
        logger.error(f"delete_monthly_price error: {e}", exc_info=True)
        # Note: Java returns status 200 (HttpStatus.OK) even on exception for Delete Fail
        return CustomResponse(data=res_body, status=200, message="Monthly Price Delete Fail")
