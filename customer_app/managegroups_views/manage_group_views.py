import logging
import os
import csv
from pathlib import Path
from typing import Any, Dict, List, Optional

from django.conf import settings
from django.db.models import Q
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated

from auth_app.authentication import CustomJWTAuthentication
from common_app.models import Group, Member, Userlist
from common_app.responses import CustomResponse
from common_app.decrypt_string import DecryptString
from common_app.common_function import CommonFunction

logger = logging.getLogger(__name__)

def write_csv(file_path: str, header: List[str], rows: List[Dict[str, Any]]) -> None:
    """Helper to write records to a CSV file in standard preference format."""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        for row in rows:
            clean_row = {}
            for col in header:
                val = row.get(col)
                if val is None:
                    clean_row[col] = ""
                else:
                    clean_row[col] = str(val)
            writer.writerow(clean_row)


def download_contacts(member_id: int, group_id: int) -> List[Dict[str, Any]]:
    """Helper to retrieve group contacts, decrypting fields and matching Java logic."""
    userlists = Userlist.objects.filter(
        groupId=group_id,
        memberId=member_id,
        status='Subscribed',
        badEmail='N',
        badPhoneNumber='N'
    ).filter(
        Q(smsStatus='Subscribed') | Q(smsStatus__isnull=True)
    ).filter(
        Q(optId__isnull=True) | Q(optId=0)
    ).order_by('firstName')

    userlist_dtos = []
    for ul in userlists:
        email_str = ""
        if ul.email and ul.email.strip():
            email_str = DecryptString.setEncDecUser(ul.email, "display", "Y") or ""

        birthday_str = ""
        if ul.birthday and ul.birthday.strip():
            try:
                decrypted_bday = DecryptString.setEncDecUser(ul.birthday, "display", "Y")
                if decrypted_bday and decrypted_bday.strip():
                    birthday_str = CommonFunction.displayDate(decrypted_bday)
            except Exception:
                birthday_str = ""

        def fmt_dt(dt) -> Optional[str]:
            return dt.strftime("%m/%d/%Y") if dt else None

        dto = {
            "emailId": ul.emailId,
            "memberId": ul.memberId,
            "firstName": ul.firstName,
            "lastName": ul.lastName,
            "birthday": birthday_str,
            "email": email_str,
            "country": ul.country if ul.country else "",
            "phoneNumber": ul.phoneNumber,
            "subMemberId": ul.subMemberId,
            "address": None,
            "age": ul.age,
            "badEmail": ul.badEmail,
            "badPhoneNumber": ul.badPhoneNumber,
            "bouncereason": ul.bounceReason,
            "cc": ul.cc,
            "city": ul.city,
            "confirmDateTime": fmt_dt(ul.confirmDateTime),
            "confirmIP": ul.confirmIP,
            "contactRating": ul.contactRating,
            "dateRegistered": fmt_dt(ul.dateRegistered),
            "dateAdded": fmt_dt(ul.dateAdded),
            "dateLastModified": fmt_dt(ul.dateLastModified),
            "dstOff": ul.dstOff,
            "emailDomain": ul.emailDomain,
            "emailClientUsed": ul.emailClientUsed,
            "emailLists": ul.emailLists,
            "emailPermissionStatusOther": ul.emailPermissionStatusOther,
            "euid": ul.euid,
            "gender": ul.gender,
            "gmtOff": ul.gmtOff,
            "isEmailValidate": ul.isEmailValidate,
            "isChecked": ul.isChecked,
            "jobTitle": ul.jobTitle,
            "latitude": ul.latitude,
            "leid": ul.leid,
            "longitude": ul.longitude,
            "notes": ul.notes,
            "optBackInDate": fmt_dt(ul.optBackInDate),
            "optDate": fmt_dt(ul.optDate),
            "optid": ul.optId,
            "optInIPAddress": ul.optInIPAddress,
            "optOutDate": fmt_dt(ul.optOutDate),
            "optOutIpAddress": ul.optOutIpAddress,
            "region": ul.region,
            "selectDateFormat": ul.selectDateFormat,
            "signupSource": ul.signupSource,
            "smsSid": ul.smsSid,
            "smsStatus": ul.smsStatus,
            "stateProvRegion": ul.stateProvRegion,
            "status": ul.status,
            "storeCustomerId": ul.storeCustomerId,
            "streetAddress": None,
            "tags": ul.tags,
            "tempCronId": ul.tempCronId,
            "timeZone": ul.timeZone,
            "udf1": ul.udf1,
            "udf10": ul.udf10,
            "udf2": ul.udf2,
            "udf3": ul.udf3,
            "udf4": ul.udf4,
            "udf5": ul.udf5,
            "udf6": ul.udf6,
            "udf7": ul.udf7,
            "udf8": ul.udf8,
            "udf9": ul.udf9,
            "usDefaultLanguage": ul.usDefaultLanguage,
            "zipPostalCode": ul.zipPostalCode
        }
        userlist_dtos.append(dto)

    return userlist_dtos


@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_group(request: Request, groupId: int) -> CustomResponse:
    """Retrieve details for a single group with decrypted createdBy details."""
    res_body: Dict[str, Any] = {}
    try:
        group = Group.objects.get(groupId=groupId)
        date_reg_str = group.dateRegistered.strftime("%m/%d/%Y") if group.dateRegistered else None

        created_by = ""
        if group.memberId:
            try:
                member = Member.objects.get(memberId=group.memberId)
                first = DecryptString.setEncDecUser(member.firstName, "display", "Y") or ""
                last = DecryptString.setEncDecUser(member.lastName, "display", "Y") or ""
                created_by = f"{first} {last}".strip()
            except Member.DoesNotExist:
                pass

        group_dto = {
            "groupId": group.groupId,
            "dateRegistered": date_reg_str,
            "ecomCustListType": group.ecomCustListType,
            "groupName": group.groupName,
            "storeName": group.storeName,
            "subMemberId": group.subMemberId,
            "memberId": group.memberId,
            "udfs": None,
            "groupSegment": None,
            "duplicateRecords": None,
            "cronId": None,
            "totalMember": None,
            "createdBy": created_by
        }
        # Clean None values to match Java's @JsonInclude(NON_NULL)
        clean_dto = {k: v for k, v in group_dto.items() if v is not None}
        res_body["group"] = clean_dto
        return CustomResponse(data=res_body, status=200, message="Group Fetched Successfully")
    except Exception as e:
        logger.error(f"getGroup error : {e}", exc_info=True)
        return CustomResponse(data=res_body, status=200, message="Group Fetch Fail")


@api_view(['DELETE'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_groups(request: Request) -> CustomResponse:
    """Bulk delete groups based on the groupIds payload."""
    res_body: Dict[str, Any] = {}
    try:
        group_ids = request.data.get("groupIds", [])
        for group_id in group_ids:
            try:
                group = Group.objects.get(groupId=group_id)
                group.delete()
            except Group.DoesNotExist:
                pass
        return CustomResponse(data=res_body, status=200, message="Groups Deleted Successfully")
    except Exception as e:
        logger.error(f"deleteGroups error : {e}", exc_info=True)
        return CustomResponse(data=res_body, status=200, message="Groups Delete Fail")


@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_group_list_page(request: Request) -> CustomResponse:
    """List groups with search and pagination support."""
    res_body: Dict[str, Any] = {}
    try:
        search_key = request.query_params.get("searchKey", "")
        page = int(request.query_params.get("page", 0))
        size = int(request.query_params.get("size", 10))

        offset = page * size
        limit = offset + size

        base_query = Group.objects.all()
        if search_key:
            base_query = base_query.filter(groupName__icontains=search_key)

        base_query = base_query.order_by('groupId')
        paginated_groups = base_query[offset:limit]

        group_dtos = []
        for group in paginated_groups:
            date_reg_str = group.dateRegistered.strftime("%m/%d/%Y") if group.dateRegistered else None

            created_by = ""
            if group.memberId:
                try:
                    member = Member.objects.get(memberId=group.memberId)
                    first = DecryptString.setEncDecUser(member.firstName, "display", "Y") or ""
                    last = DecryptString.setEncDecUser(member.lastName, "display", "Y") or ""
                    created_by = f"{first} {last}".strip()
                except Member.DoesNotExist:
                    pass

            group_dto = {
                "groupId": group.groupId,
                "dateRegistered": date_reg_str,
                "ecomCustListType": group.ecomCustListType,
                "groupName": group.groupName,
                "storeName": group.storeName,
                "subMemberId": group.subMemberId,
                "memberId": group.memberId,
                "udfs": None,
                "groupSegment": None,
                "duplicateRecords": None,
                "cronId": None,
                "totalMember": None,
                "createdBy": created_by
            }
            clean_dto = {k: v for k, v in group_dto.items() if v is not None}
            group_dtos.append(clean_dto)

        res_body["groupListPage"] = group_dtos
        res_body["getTotalRecords"] = Group.objects.count()
        return CustomResponse(data=res_body, status=200, message="Group List Fetched Successfully")
    except Exception as e:
        logger.error(f"getGroupListPage error : {e}", exc_info=True)
        return CustomResponse(data=res_body, status=200, message="Group List Fetch Fail")


@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_download_contact_file(request: Request, groupId: int, memberId: int) -> CustomResponse:
    """Export group contacts to a CSV download file."""
    res_body: Dict[str, Any] = {}
    try:
        userlist_dtos = download_contacts(memberId, groupId)

        csv_download_path = getattr(settings, 'CSVDOWNLOAD_DIR', None)
        if not csv_download_path:
            csv_download_path = settings.BASE_DIR / 'csv_download'
        else:
            csv_download_path = Path(csv_download_path)

        file_path = str(csv_download_path / f"export_csv_{memberId}.csv")
        site_url = getattr(settings, 'SITEURL', 'https://samsa.salesandmarketing.ai/')

        res_body["filePath"] = f"{site_url}csv_download/export_csv_{memberId}.csv"

        name_mapping = [
            "emailId", "memberId", "firstName", "lastName", "birthday", "email", "country", "phoneNumber",
            "subMemberId", "address", "age", "badEmail", "badPhoneNumber", "bouncereason", "cc", "city",
            "confirmDateTime", "confirmIP", "contactRating", "dateRegistered", "dateAdded", "dateLastModified",
            "dstOff", "emailDomain", "emailClientUsed", "emailLists", "emailPermissionStatusOther", "euid",
            "gender", "gmtOff", "isEmailValidate", "isChecked", "jobTitle", "latitude", "leid", "longitude",
            "notes", "optBackInDate", "optDate", "optid", "optInIPAddress", "optOutDate", "optOutIpAddress",
            "region", "selectDateFormat", "signupSource", "smsSid", "smsStatus", "stateProvRegion", "status",
            "storeCustomerId", "streetAddress", "tags", "tempCronId", "timeZone", "udf1", "udf10", "udf2", "udf3",
            "udf4", "udf5", "udf6", "udf7", "udf8", "udf9", "usDefaultLanguage", "zipPostalCode"
        ]

        write_csv(file_path, name_mapping, userlist_dtos)
        return CustomResponse(data=res_body, status=200, message="Export contact successfully.")
    except Exception as e:
        logger.error(f"getDownloadContactFile error : {e}", exc_info=True)
        return CustomResponse(data=res_body, status=500, message="Export contact failed.")
