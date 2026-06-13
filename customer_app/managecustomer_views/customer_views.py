import logging
import math
from typing import Any, Dict, Optional

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated

from auth_app.authentication import CustomJWTAuthentication
from common_app.models import Userlist
from common_app.responses import CustomResponse
from common_app.decrypt_string import DecryptString


logger = logging.getLogger(__name__)


def serialize_customer(userlist: Userlist) -> Dict[str, Any]:
    """Helper to convert Userlist to a CustomerDto dictionary, removing null keys."""
    email_str = ""
    if userlist.email and userlist.email.strip():
        try:
            email_str = DecryptString.setEncDecUser(userlist.email, "display", "Y") or ""
        except Exception:
            email_str = ""

    raw_dto = {
        "emailId": userlist.emailId,
        "memberId": userlist.memberId,
        "firstName": userlist.firstName,
        "lastName": userlist.lastName,
        "email": email_str,
        "udf1": userlist.udf1,
        "udf2": userlist.udf2,
        "udf3": userlist.udf3,
        "udf4": userlist.udf4,
        "udf5": userlist.udf5,
        "udf6": userlist.udf6,
        "udf7": userlist.udf7,
        "udf8": userlist.udf8,
        "udf9": userlist.udf9,
        "udf10": userlist.udf10,
    }
    return {k: v for k, v in raw_dto.items() if v is not None}


@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_customer_list_page(request: Request, searchKey: Optional[str] = None) -> CustomResponse:
    """Lists customer userlists with search on firstName and pagination metrics."""
    res_body: Dict[str, Any] = {}
    try:
        search_key = searchKey or request.query_params.get("searchKey", "")
        page = int(request.query_params.get("page", 0))
        size = int(request.query_params.get("size", 10))

        offset = page * size
        limit = offset + size

        base_query = Userlist.objects.all().order_by('emailId')
        if search_key:
            # Match Java repository: lower(firstName) like lower(CONCAT('%', :searchKey, '%'))
            base_query = base_query.filter(firstName__icontains=search_key)

        total_records = Userlist.objects.count()
        filtered_count = base_query.count()
        total_pages = math.ceil(filtered_count / size) if size > 0 else 0

        paginated_users = base_query[offset:limit]
        customer_dtos = [serialize_customer(user) for user in paginated_users]

        res_body["getTotalPages"] = total_pages
        res_body["getNumber"] = page
        res_body["getSize"] = size
        res_body["customerListPage"] = customer_dtos
        res_body["getTotalRecords"] = total_records

        return CustomResponse(data=res_body, status=200, message="Customer List Page Fetched Successfully")
    except Exception as e:
        logger.error(f"getCustomerListPage error : {e}", exc_info=True)
        return CustomResponse(data=res_body, status=500, message="Customer List Page Fetch Fail")


@api_view(['DELETE'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_customers(request: Request) -> CustomResponse:
    """Bulk deletes customer staging/userlist records based on a list of email IDs."""
    res_body: Dict[str, Any] = {}
    try:
        # Request body parameters matches DeleteCustomerDto (contains list of emailIds)
        email_ids = request.data.get("emailIds", [])
        if email_ids:
            Userlist.objects.filter(emailId__in=email_ids).delete()
        return CustomResponse(data=res_body, status=200, message="Customers Deleted Successfully")
    except Exception as e:
        logger.error(f"deleteCustomers error : {e}", exc_info=True)
        return CustomResponse(data=res_body, status=200, message="Customer Delete Fail")
