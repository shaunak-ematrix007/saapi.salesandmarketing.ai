import logging
import re
from typing import Any, Dict, List, Optional, Set
from django.db import connection, models
from django.db.models import Q
from django.utils import timezone
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated

from auth_app.authentication import CustomJWTAuthentication
from common_app.models import GroupSegment, GroupSegmentField, Userlist
from common_app.responses import CustomResponse
from common_app.decrypt_string import DecryptString
from common_app.common_function import CommonFunction

logger = logging.getLogger(__name__)

CONTACT_HEADER_KEYS = [
    "firstName", "lastName", "email", "phoneNumber", "usDefaultLanguage", "status",
    "dateRegistered", "optid", "optDate", "bouncereason", "optBackInDate", "optOutDate",
    "streetAddress", "address", "city", "state", "zipPostalCode", "country", "birthday",
    "gender", "dateAdded", "dateLastModified", "signupSource", "contactRating", "optInIPAddress",
    "confirmIP", "confirmDateTime", "optOutIpAddress", "latitude", "longitude", "gmtOff",
    "dstOff", "timeZone", "region", "notes", "tags", "emailClientUsed", "emailDomain", "cc",
    "leid", "euid", "age", "smsStatus", "jobTitle", "emailPermissionStatusOther", "emailLists"
]

CONTACT_HEADER_VALUES = [
    "First Name", "Last Name", "Email", "Mobile", "Language", "Status",
    "Registered Date", "Opt Id", "Opt Date", "Bounce Reason", "Opt Back In Date", "Opt Out Date",
    "Street Address", "Address", "City", "State", "Zip Code", "Country", "Birthday",
    "Gender", "Added Date", "Last Modified Date", "Signup Source", "Contact Rating", "Opt In IP Address",
    "Confirm IP", "Confirm Date Time", "Opt Out IP Address", "Latitude", "Longitude", "GMTOff",
    "DSTOff", "Timezone", "Region", "Notes", "Tags", "Email Client Used", "Email Domain", "CC",
    "LEID", "EUID", "Age", "SMS Status", "Job Title", "Email Permission Status - Other", "Email Lists"
]


def get_segment_total_member(segment_id: int) -> int:
    """Helper to run a segments raw SQL query replacing SELECT * with COUNT."""
    try:
        segment = GroupSegment.objects.get(segId=segment_id)
        sql = segment.segQuery
        if not sql:
            return 0
        sql_count = re.sub(r'(?i)select\s+\*', 'SELECT count(*)', sql)
        with connection.cursor() as cursor:
            cursor.execute(sql_count)
            row = cursor.fetchone()
            return row[0] if row else 0
    except Exception:
        return 0


def find_segment_list(group_id: int, member_id: int) -> List[Dict[str, Any]]:
    """Helper to retrieve group segments and count active members in each segment."""
    segments = GroupSegment.objects.filter(groupId=group_id, memberId=member_id)
    segment_list = []
    for seg in segments:
        total_member = get_segment_total_member(seg.segId)
        segment_list.append({
            "segId": seg.segId,
            "segName": seg.segName,
            "totalMember": total_member
        })
    return segment_list


def create_and_update_group_segment(group_segment_dto: Dict[str, Any], member_id: int) -> GroupSegment:
    """Consolidates logic to save segment metadata, dynamically construct the SQL query, and store conditions."""
    seg_id = group_segment_dto.get("segId")
    if seg_id:
        segment = GroupSegment.objects.filter(segId=seg_id).first()
        if segment:
            GroupSegmentField.objects.filter(segId=seg_id).delete()
        else:
            segment = GroupSegment()
    else:
        segment = GroupSegment()

    segment.segName = group_segment_dto.get("segName")
    segment.groupId = group_segment_dto.get("groupId")
    segment.memberId = member_id
    segment.subMemberId = group_segment_dto.get("subMemberId", 0)
    segment.segDateAdded = timezone.now()

    sub_query = f"select * from tbl_userlist WHERE group_id = {segment.groupId} AND Member_Id = {segment.memberId} AND (BadEmail = 'N' and BadPhoneNumber = 'N' and (optid is null or optid=0)) AND Status = 'Subscribed' AND (smsStatus='Subscribed' or smsStatus is null) AND  (   "
    sub_field_query = ""

    field_dtos = group_segment_dto.get("groupSegmentFieldDtos", [])
    sorted_fields = sorted(field_dtos, key=lambda x: x.get("segDisplayOrder", 0))

    for field_dto in sorted_fields:
        seg_conditions = field_dto.get("segConditions")
        if seg_conditions:
            sub_field_query += seg_conditions + " "

        field_name = field_dto.get("segFieldName")
        field_operator = field_dto.get("segFieldOperator", "")

        if field_name == "Email":
            sub_field_query += "email_domain " + field_operator
        else:
            sub_field_query += field_name + " " + field_operator

        field_val = field_dto.get("segFieldValue", "")
        if field_operator.strip().lower() == "like":
            sub_field_query += f" '%{field_val}%' "
        else:
            sub_field_query += f" '{field_val}' "

    segment.segQuery = sub_query + sub_field_query + " )"
    segment.save()

    for field_dto in sorted_fields:
        GroupSegmentField.objects.create(
            segId=segment.segId,
            segFieldName=field_dto.get("segFieldName"),
            segFieldOperator=field_dto.get("segFieldOperator"),
            segFieldValue=field_dto.get("segFieldValue"),
            segConditions=field_dto.get("segConditions"),
            segDisplayOrder=field_dto.get("segDisplayOrder")
        )

    return segment


def get_val(row: Dict[str, Any], key: str, default: Any = None) -> Any:
    """Helper to retrieve SQL row keys case-insensitively."""
    for k, v in row.items():
        if k.lower() == key.lower():
            return v
    return default


def serialize_rs_contact(row: Dict[str, Any], dup_emails_set: Set[str], dup_phones_set: Set[str]) -> Dict[str, Any]:
    """Helper to convert dynamic SQL cursor results to serialized camelCase contact representations."""
    dup_records = "N"

    raw_email = get_val(row, "Email", "")
    email_str = ""
    if raw_email and raw_email.strip():
        try:
            email_str = DecryptString.setEncDecUser(raw_email, "display", "Y") or ""
        except Exception:
            email_str = ""
        if raw_email in dup_emails_set:
            dup_records = "Y"

    phone_number = get_val(row, "phoneNumber", "")
    if phone_number and phone_number in dup_phones_set:
        dup_records = "Y"

    birthday_str = ""
    raw_birthday = get_val(row, "birthday", "")
    if raw_birthday and raw_birthday.strip():
        try:
            decrypted_bday = DecryptString.setEncDecUser(raw_birthday, "display", "Y")
            if decrypted_bday and decrypted_bday.strip():
                from datetime import datetime
                try:
                    bday_dt = datetime.strptime(decrypted_bday, "%Y-%m-%d")
                    birthday_str = bday_dt.strftime("%m/%d/%Y")
                except ValueError:
                    birthday_str = decrypted_bday
        except Exception:
            birthday_str = ""

    def format_date(dt_val) -> Optional[str]:
        if dt_val is None:
            return None
        if isinstance(dt_val, str):
            return dt_val
        return dt_val.strftime("%Y-%m-%d %H:%M:%S")

    dto = {
        "duplicateRecords": dup_records,
        "emailId": get_val(row, "Email_Id"),
        "memberId": get_val(row, "Member_id"),
        "firstName": get_val(row, "First_Name"),
        "lastName": get_val(row, "Last_Name"),
        "email": email_str,
        "udf1": get_val(row, "udf1"),
        "udf2": get_val(row, "udf2"),
        "udf3": get_val(row, "udf3"),
        "udf4": get_val(row, "udf4"),
        "udf5": get_val(row, "udf5"),
        "udf6": get_val(row, "udf6"),
        "udf7": get_val(row, "udf7"),
        "udf8": get_val(row, "udf8"),
        "udf9": get_val(row, "udf9"),
        "udf10": get_val(row, "udf10"),
        "status": get_val(row, "Status"),
        "dateRegistered": format_date(get_val(row, "Date_Registered")),
        "badEmail": get_val(row, "BadEmail"),
        "isChecked": get_val(row, "IsChecked"),
        "optid": get_val(row, "optid"),
        "bouncereason": get_val(row, "bouncereason"),
        "tempCronId": get_val(row, "temp_cron_id"),
        "birthday": birthday_str,
        "smsStatus": get_val(row, "smsStatus"),
        "smsSid": get_val(row, "smsSid"),
        "streetAddress": get_val(row, "streetAddress"),
        "address": get_val(row, "address"),
        "stateProvRegion": get_val(row, "stateProvRegion"),
        "zipPostalCode": get_val(row, "zipPostalCode"),
        "country": get_val(row, "country"),
        "gender": get_val(row, "gender"),
        "dateAdded": format_date(get_val(row, "dateAdded")),
        "dateLastModified": format_date(get_val(row, "dateLastModified")),
        "signupSource": get_val(row, "signupSource"),
        "contactRating": get_val(row, "contactRating"),
        "optInIPAddress": get_val(row, "optInIPAddress"),
        "confirmIP": get_val(row, "confirmIP"),
        "optOutIpAddress": get_val(row, "optOutIpAddress"),
        "latitude": get_val(row, "latitude"),
        "longitude": get_val(row, "longitude"),
        "gmtOff": get_val(row, "gmtOff"),
        "dstOff": get_val(row, "dstOff"),
        "timeZone": get_val(row, "timeZone"),
        "region": get_val(row, "region"),
        "notes": get_val(row, "notes"),
        "tags": get_val(row, "tags"),
        "emailClientUsed": get_val(row, "emailClientUsed"),
        "phoneNumber": phone_number,
        "emailDomain": get_val(row, "email_domain"),
        "cc": get_val(row, "CC"),
        "leid": get_val(row, "LEID"),
        "euid": get_val(row, "EUID"),
        "age": get_val(row, "age"),
        "jobTitle": get_val(row, "jobTitle"),
        "emailPermissionStatusOther": get_val(row, "emailPermissionStatusOther"),
        "emailLists": get_val(row, "emailLists"),
        "selectDateFormat": get_val(row, "selectDateFormat"),
        "badPhoneNumber": get_val(row, "BadPhoneNumber"),
        "usDefaultLanguage": get_val(row, "us_default_language"),
        "isEmailValidate": get_val(row, "is_email_validate"),
        "storeCustomerId": get_val(row, "store_customer_id"),
        "subMemberId": get_val(row, "sub_member_id")
    }
    return {k: v for k, v in dto.items() if v is not None}


@api_view(['POST'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def create_group_segment(request: Request) -> CustomResponse:
    """View to create a new group segment and associated filter fields."""
    res_body: Dict[str, Any] = {}
    try:
        member_id = CommonFunction.getFinalMemberId(request.user)
        group_segment_dto = request.data

        # Payload validations
        field_dtos = group_segment_dto.get("groupSegmentFieldDtos", [])
        for field_dto in field_dtos:
            if not field_dto.get("segFieldName"):
                return CustomResponse(data=res_body, status=500, message="Please select segment field")
            if not field_dto.get("segFieldValue"):
                return CustomResponse(data=res_body, status=500, message="Please select segment field value")

        segment = create_and_update_group_segment(group_segment_dto, member_id)
        res_body["segId"] = segment.segId
        return CustomResponse(data=res_body, status=200, message="Segment added successfully.")
    except Exception as e:
        logger.error(f"createGroupSegment error: {e}", exc_info=True)
        return CustomResponse(data=res_body, status=500, message="error")


@api_view(['PUT'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def update_group_segment(request: Request, segmentId: int) -> CustomResponse:
    """View to update an existing group segment and reconstruct the saved query string."""
    res_body: Dict[str, Any] = {}
    try:
        member_id = CommonFunction.getFinalMemberId(request.user)
        group_segment_dto = request.data
        group_segment_dto["segId"] = segmentId

        # Payload validations
        field_dtos = group_segment_dto.get("groupSegmentFieldDtos", [])
        for field_dto in field_dtos:
            if not field_dto.get("segFieldName"):
                return CustomResponse(data=res_body, status=500, message="Please select segment field")
            if not field_dto.get("segFieldValue"):
                return CustomResponse(data=res_body, status=500, message="Please select segment field value")

        create_and_update_group_segment(group_segment_dto, member_id)
        return CustomResponse(data=res_body, status=200, message="Segment updated successfully.")
    except Exception as e:
        logger.error(f"updateGroupSegment error: {e}", exc_info=True)
        return CustomResponse(data=res_body, status=500, message="error")


@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_segment(request: Request, segmentId: int) -> CustomResponse:
    """Retrieves metadata and filter condition fields for a segment ID."""
    try:
        segment = GroupSegment.objects.filter(segId=segmentId).first()
        if not segment:
            return CustomResponse(data=None, status=500, message="Segment not found")

        fields = GroupSegmentField.objects.filter(segId=segmentId).order_by('segDisplayOrder')
        field_dtos = [{
            "segfId": f.segfId,
            "segId": f.segId,
            "segFieldName": f.segFieldName,
            "segFieldOperator": f.segFieldOperator,
            "segFieldValue": f.segFieldValue,
            "segConditions": f.segConditions,
            "segDisplayOrder": f.segDisplayOrder
        } for f in fields]

        seg_added_date_str = segment.segDateAdded.strftime("%m/%d/%Y") if segment.segDateAdded else None

        dto = {
            "segId": segment.segId,
            "segName": segment.segName,
            "groupId": segment.groupId,
            "memberId": segment.memberId,
            "segQuery": segment.segQuery,
            "segAddedDate": seg_added_date_str,
            "subMemberId": segment.subMemberId,
            "groupSegmentFieldDtos": field_dtos
        }
        dto = {k: v for k, v in dto.items() if v is not None}
        return CustomResponse(data=dto, status=200, message="Segment fetched successfully.")
    except Exception as e:
        logger.error(f"getSegment error: {e}", exc_info=True)
        return CustomResponse(data=None, status=500, message="error")


@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_segment_list(request: Request, groupId: int) -> CustomResponse:
    """Lists segments mapped to a groupId alongside member count summaries."""
    try:
        member_id = CommonFunction.getFinalMemberId(request.user)
        segment_dtos = find_segment_list(groupId, member_id)
        return CustomResponse(data=segment_dtos, status=200, message="Segment fetched successfully.")
    except Exception as e:
        logger.error(f"getSegmentList error: {e}", exc_info=True)
        return CustomResponse(data=None, status=500, message="error")


@api_view(['DELETE'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_bulk_segment(request: Request) -> CustomResponse:
    """Deletes list of segment IDs in bulk."""
    res_body: Dict[str, Any] = {}
    try:
        seg_ids = request.data.get("segIds", [])
        if seg_ids:
            GroupSegmentField.objects.filter(segId__in=seg_ids).delete()
            GroupSegment.objects.filter(segId__in=seg_ids).delete()
            return CustomResponse(data=res_body, status=200, message="Segment deleted successfully.")
        else:
            return CustomResponse(data=res_body, status=500, message="error")
    except Exception as e:
        logger.error(f"deleteBulkSegment error: {e}", exc_info=True)
        return CustomResponse(data=res_body, status=500, message="error")


@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_segment_contact_list(request: Request, groupId: int, segmentId: int) -> CustomResponse:
    """Retrieves header dictionaries and parses contact objects matched by the segment's dynamic filters."""
    res_body: Dict[str, Any] = {}
    try:
        member_id = CommonFunction.getFinalMemberId(request.user)

        # Header definitions matching Group UDF lists
        from common_app.models import Udf
        keys = list(CONTACT_HEADER_KEYS)
        udfs = Udf.objects.filter(groupId=groupId).order_by('udfLabel')
        for u in udfs:
            keys.append(f"udf{u.udfLabel}")

        headers_dict = {}
        for k, v in zip(CONTACT_HEADER_KEYS, CONTACT_HEADER_VALUES):
            headers_dict[k] = v
        for u in udfs:
            headers_dict[f"udf{u.udfLabel}"] = u.udf

        res_body["contactHeaderKey"] = keys
        res_body["contactHeader"] = headers_dict

        segment = GroupSegment.objects.filter(segId=segmentId).first()
        if not segment or not segment.segQuery:
            res_body["contact"] = []
            res_body["getTotalPages"] = None
            res_body["getNumber"] = None
            res_body["getSize"] = None
            res_body["totalContact"] = 0
            return CustomResponse(data=res_body, status=200, message="Segment fetched successfully.")

        # Find duplicate phones/emails in this group to flag entries
        sub_qs = Userlist.objects.filter(
            groupId=groupId,
            memberId=member_id,
            status='Subscribed',
            badEmail='N',
            badPhoneNumber='N'
        ).filter(
            Q(smsStatus='Subscribed') | Q(smsStatus__isnull=True)
        ).filter(
            Q(optId__isnull=True) | Q(optId=0)
        )

        dup_emails = sub_qs.exclude(email='').exclude(email__isnull=True)\
                           .values('email')\
                           .annotate(count=models.Count('emailId'))\
                           .filter(count__gt=1)\
                           .values_list('email', flat=True)

        dup_phones = sub_qs.exclude(phoneNumber='').exclude(phoneNumber__isnull=True)\
                           .values('phoneNumber')\
                           .annotate(count=models.Count('emailId'))\
                           .filter(count__gt=1)\
                           .values_list('phoneNumber', flat=True)

        dup_emails_set = set(dup_emails)
        dup_phones_set = set(dup_phones)

        sql = segment.segQuery
        sql += " ORDER BY tul.First_Name ASC"

        contacts_raw = []
        with connection.cursor() as cursor:
            cursor.execute(sql)
            columns = [col[0] for col in cursor.description]
            for row in cursor.fetchall():
                row_dict = dict(zip(columns, row))
                contacts_raw.append(row_dict)

        contact_dtos = [serialize_rs_contact(c, dup_emails_set, dup_phones_set) for c in contacts_raw]

        res_body["contact"] = contact_dtos
        res_body["getTotalPages"] = None
        res_body["getNumber"] = None
        res_body["getSize"] = None
        res_body["totalContact"] = len(contact_dtos)

        return CustomResponse(data=res_body, status=200, message="Segment fetched successfully.")
    except Exception as e:
        logger.error(f"getSegmentContactList error: {e}", exc_info=True)
        return CustomResponse(data=res_body, status=500, message="error")
