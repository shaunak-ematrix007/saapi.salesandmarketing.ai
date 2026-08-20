import logging
import math
from typing import Any, Dict

from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.status import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR

from common_app.models import CampaignTransaction, Invoice, Tenants
from common_app.responses import CustomResponse

logger = logging.getLogger(__name__)

def serialize_campaign_transaction(ct: CampaignTransaction) -> Dict[str, Any]:
    """Helper to convert CampaignTransaction model instance to a camelCase dictionary."""
    tran_campaign_date_str = None
    if ct.tranCampaignDate:
        tran_campaign_date_str = ct.tranCampaignDate.strftime('%Y-%m-%d %H:%M:%S')

    tran_invoiced_date_str = None
    if ct.tranInvoicedDate:
        tran_invoiced_date_str = ct.tranInvoicedDate.strftime('%Y-%m-%d')

    return {
        "tranId": ct.tranId,
        "tranCampaignId": ct.tranCampaignId,
        "tranCampaignName": ct.tranCampaignName,
        "tranCampaignDate": tran_campaign_date_str,
        "tranTotalMember": ct.tranTotalMember,
        "tranType": ct.tranType,
        "tranInvoicedId": ct.tranInvoicedId,
        "tranInvoicedStatus": ct.tranInvoicedStatus,
        "tranInvoicedDate": tran_invoiced_date_str,
        "memberId": ct.memberId,
        "tranBillType": ct.tranBillType,
        "tranTotalAmount": ct.tranTotalAmount,
        "tranMemberRate": ct.tranMemberRate,
        "tranCountTotalSms": ct.tranCountTotalSms,
        "tranPollFormNo": ct.tranPollFormNo,
        "tranPollToNo": ct.tranPollToNo,
        "subMemberId": ct.subMemberId,
    }

@api_view(['GET'])
def get_uninvoice_members(request: Request) -> CustomResponse:
    """Returns members who have a membershipType value, with their names decrypted."""
    try:
        members = Tenants.objects.select_related('details').filter(details__td_membership_type__isnull=False)
        member_dtos = []
        for member in members:
            first_name_dec = member.ten_first_name or ""
            last_name_dec = member.ten_last_name or ""
            full_name = f"{first_name_dec} {last_name_dec}".strip()
            member_dtos.append({
                "memberId": member.ten_id,
                "memberFullName": full_name
            })
        
        res_body = {
            "uninvoiceMembers": member_dtos
        }
        return CustomResponse(data=res_body, status=HTTP_200_OK, message="Uninvoice Members Fetched Successfully")
    except Exception as e:
        logger.error(f"getUninvoiceMembers error: {e}", exc_info=True)
        return CustomResponse(data={}, status=HTTP_500_INTERNAL_SERVER_ERROR, message="Internal Server Error")

@api_view(['GET'])
def get_uninvoice_list_page(request: Request) -> CustomResponse:
    """Returns a paginated list of all uninvoiced transactions."""
    try:
        search_key = request.query_params.get("searchKey", "")
        page = int(request.query_params.get("page", 0))
        size = int(request.query_params.get("size", 10))
        
        offset = page * size
        limit = offset + size
        
        base_query = CampaignTransaction.objects.filter(tranInvoicedStatus='uninvoiced', tranBillType='0')
        
        if search_key:
            base_query = base_query.filter(tranCampaignName__icontains=search_key)
            
        base_query = base_query.order_by('-tranId')
        
        total_query_count = base_query.count()
        paginated_transactions = base_query[offset:limit]
        
        total_pages = math.ceil(total_query_count / size) if size > 0 else 0
        total_records = Invoice.objects.count()
        
        transaction_dtos = [serialize_campaign_transaction(ct) for ct in paginated_transactions]
        
        res_body = {
            "getTotalPages": total_pages,
            "getNumber": page,
            "getSize": size,
            "uninvoiceListPage": transaction_dtos,
            "getTotalRecords": total_records
        }
        return CustomResponse(data=res_body, status=HTTP_200_OK, message="Uninvoice List Fetched Successfully")
    except Exception as e:
        logger.error(f"getUninvoiceListPage error: {e}", exc_info=True)
        return CustomResponse(data={}, status=HTTP_500_INTERNAL_SERVER_ERROR, message="Internal Server Error")

@api_view(['GET'])
def get_uninvoice_list_page_with_id(request: Request) -> CustomResponse:
    """Returns a paginated list of uninvoiced transactions for a specific member."""
    try:
        search_key = request.query_params.get("searchKey", "")
        page = int(request.query_params.get("page", 0))
        size = int(request.query_params.get("size", 10))
        member_id_str = request.query_params.get("memberId")
        
        if not member_id_str:
            return CustomResponse(data={}, status=HTTP_500_INTERNAL_SERVER_ERROR, message="Member ID is required")
            
        member_id = int(member_id_str)
        offset = page * size
        limit = offset + size
        
        base_query = CampaignTransaction.objects.filter(memberId=member_id, tranInvoicedStatus='uninvoiced', tranBillType='0')
        
        if search_key:
            base_query = base_query.filter(tranCampaignName__icontains=search_key)
            
        base_query = base_query.order_by('-tranId')
        
        total_query_count = base_query.count()
        paginated_transactions = base_query[offset:limit]
        
        total_pages = math.ceil(total_query_count / size) if size > 0 else 0
        
        total_uninvoiced_records = CampaignTransaction.objects.filter(memberId=member_id).count()
        
        transaction_dtos = [serialize_campaign_transaction(ct) for ct in paginated_transactions]
        
        res_body = {
            "getTotalPages": total_pages,
            "getNumber": page,
            "getSize": size,
            "uninvoiceListPage": transaction_dtos,
            "getTotalRecords": total_uninvoiced_records
        }
        return CustomResponse(data=res_body, status=HTTP_200_OK, message="Uninvoice List Fetched Successfully")
    except Exception as e:
        logger.error(f"getUninvoiceListPageWithId error: {e}", exc_info=True)
        return CustomResponse(data={}, status=HTTP_500_INTERNAL_SERVER_ERROR, message="Internal Server Error")
