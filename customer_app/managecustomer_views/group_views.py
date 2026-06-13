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
from common_app.models import Group, Userlist, Udf, TempCronUserListTotal, GroupSegment
from common_app.responses import CustomResponse
from common_app.decrypt_string import DecryptString
from common_app.common_function import CommonFunction

logger = logging.getLogger(__name__)

UDF_KEYS = [
    "First_Name", "Last_Name", "Email", "phoneNumber", "streetAddress",
    "address", "city", "stateProvRegion", "zipPostalCode", "region",
    "gender", "age", "contactRating", "tags"
]

UDF_VALUES = [
    "First Name", "Last Name", "Email", "Mobile Number", "Street Address",
    "Address", "City", "State", "Zip Code", "Region",
    "Gender", "Age", "Contact Rating", "Tags"
]

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


def count_total_contact(member_id: int, group_id: Optional[int] = None) -> int:
    """Helper to calculate total subscribed contacts for a member, optionally filtered by group."""
    q = Userlist.objects.filter(
        memberId=member_id,
        status='Subscribed',
        badEmail='N',
        badPhoneNumber='N'
    ).filter(
        Q(smsStatus='Subscribed') | Q(smsStatus__isnull=True)
    ).filter(
        Q(optId__isnull=True) | Q(optId=0)
    )
    if group_id is not None:
        q = q.filter(groupId=group_id)
    return q.count()


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


def get_udf_val(userlist: Userlist, label: int) -> str:
    """Helper to dynamically fetch a udf field value from Userlist."""
    attr = f"udf{label}"
    return getattr(userlist, attr, "") or ""


def serialize_group(group: Group, member_id: int) -> Dict[str, Any]:
    """Helper to serialize a Group model to matched camelCase structure."""
    total_member = count_total_contact(member_id, group.groupId)
    group_segments = find_segment_list(group.groupId, member_id)

    sub_qs = Userlist.objects.filter(
        groupId=group.groupId,
        memberId=member_id,
        status='Subscribed',
        badEmail='N',
        badPhoneNumber='N'
    ).filter(
        Q(smsStatus='Subscribed') | Q(smsStatus__isnull=True)
    ).filter(
        Q(optId__isnull=True) | Q(optId=0)
    )

    has_dup_email = sub_qs.exclude(email='').exclude(email__isnull=True)\
                          .values('email')\
                          .annotate(count=models.Count('emailId'))\
                          .filter(count__gt=1)\
                          .exists()

    has_dup_phone = sub_qs.exclude(phoneNumber='').exclude(phoneNumber__isnull=True)\
                          .values('phoneNumber')\
                          .annotate(count=models.Count('emailId'))\
                          .filter(count__gt=1)\
                          .exists()

    duplicate_records = 'Y' if (has_dup_email or has_dup_phone) else 'N'

    cron_id = TempCronUserListTotal.objects.filter(
        cronGroupId=group.groupId,
        cronProcessFinished='N',
        cronMemberId=member_id
    ).values_list('cronId', flat=True).first() or 0

    date_registered_str = group.dateRegistered.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3] if group.dateRegistered else None

    group_dto = {
        "groupId": group.groupId,
        "groupName": group.groupName,
        "storeName": group.storeName,
        "ecomCustListType": group.ecomCustListType,
        "dateRegistered": date_registered_str,
        "subMemberId": group.subMemberId,
        "memberId": group.memberId,
        "totalMember": total_member,
        "groupSegment": group_segments,
        "duplicateRecords": duplicate_records,
        "cronId": cron_id
    }
    return {k: v for k, v in group_dto.items() if v is not None}


@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_group_list(request: Request) -> CustomResponse:
    """Retrieve list of groups along with counts, segments, duplicate flags and total contacts."""
    res_body: Dict[str, Any] = {}
    try:
        member_id = CommonFunction.getFinalMemberId(request.user)
        groups = Group.objects.filter(memberId=member_id).order_by('groupName')
        
        group_dtos = [serialize_group(gp, member_id) for gp in groups]
        if group_dtos:
            res_body["group"] = group_dtos

        # Count total contact across all groups of this member
        group_ids = groups.values_list('groupId', flat=True)
        total_contact = Userlist.objects.filter(
            memberId=member_id,
            groupId__in=group_ids,
            status='Subscribed',
            badEmail='N',
            badPhoneNumber='N'
        ).filter(
            Q(smsStatus='Subscribed') | Q(smsStatus__isnull=True)
        ).filter(
            Q(optId__isnull=True) | Q(optId=0)
        ).count()

        res_body["totalContact"] = total_contact
        return CustomResponse(data=res_body, status=200, message="Group fetched successfully.")
    except Exception as e:
        logger.error(f"getGroupList error: {e}", exc_info=True)
        return CustomResponse(data=res_body, status=500, message="error")


@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_group(request: Request, groupId: int) -> CustomResponse:
    """Retrieve specific group by ID."""
    try:
        group = Group.objects.filter(groupId=groupId).first()
        if group:
            date_registered_str = group.dateRegistered.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3] if group.dateRegistered else None
            group_dto = {
                "groupId": group.groupId,
                "groupName": group.groupName,
                "storeName": group.storeName,
                "ecomCustListType": group.ecomCustListType,
                "dateRegistered": date_registered_str,
                "subMemberId": group.subMemberId,
                "memberId": group.memberId
            }
            group_dto = {k: v for k, v in group_dto.items() if v is not None}
            return CustomResponse(data=group_dto, status=200, message="Group fetched successfully.")
        else:
            return CustomResponse(data=None, status=200, message="Group fetched successfully.")
    except Exception as e:
        logger.error(f"getGroup error: {e}", exc_info=True)
        return CustomResponse(data=None, status=500, message="error")


@api_view(['POST'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def save_group(request: Request) -> CustomResponse:
    """Creates or updates a group and its associated user-defined custom fields (UDFs)."""
    res_body: Dict[str, Any] = {}
    try:
        member_id = CommonFunction.getFinalMemberId(request.user)
        group_name = request.data.get("groupName")
        group_id = int(request.data.get("groupId", 0))

        # Check if group name already exists for member
        if group_id == 0:
            exists = Group.objects.filter(memberId=member_id, groupName=group_name).exists()
        else:
            exists = Group.objects.filter(memberId=member_id, groupName=group_name).exclude(groupId=group_id).exists()

        if exists:
            return CustomResponse(data=res_body, status=304, message="Group name already in used.")

        if group_id == 0:
            group = Group.objects.create(
                groupName=group_name,
                storeName=request.data.get("storeName"),
                ecomCustListType=request.data.get("ecomCustListType"),
                memberId=member_id,
                subMemberId=int(request.data.get("subMemberId", 0)),
                dateRegistered=timezone.now()
            )
        else:
            group = Group.objects.get(groupId=group_id)
            group.groupName = group_name
            group.storeName = request.data.get("storeName")
            group.ecomCustListType = request.data.get("ecomCustListType")
            group.memberId = member_id
            group.subMemberId = int(request.data.get("subMemberId", 0))
            group.save()

        # Handle UDF mappings
        udfs_payload = request.data.get("udfs", [])
        if udfs_payload:
            seen_udfs = set()
            unique_udfs = []
            for udf_data in udfs_payload:
                u_val = udf_data.get("udf", "").strip()
                if u_val and u_val not in seen_udfs:
                    seen_udfs.add(u_val)
                    unique_udfs.append(udf_data)

            i = 1
            for udf_data in unique_udfs:
                udf_name = udf_data.get("udf", "").strip()
                check_udf = Udf.objects.filter(groupId=group.groupId, udf=udf_name).exists()
                if not check_udf:
                    Udf.objects.create(
                        groupId=group.groupId,
                        udf=udf_name,
                        udfLabel=i
                    )
                i += 1

        if group_id == 0:
            return CustomResponse(data=res_body, status=200, message="Add group successfully.")
        else:
            return CustomResponse(data=res_body, status=200, message="Update group successfully.")
    except Exception as e:
        logger.error(f"saveGroup error: {e}", exc_info=True)
        return CustomResponse(data=res_body, status=500, message="error")


@api_view(['DELETE'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_bulk_group(request: Request) -> CustomResponse:
    """Deletes groups in bulk for the authenticated member."""
    res_body: Dict[str, Any] = {}
    try:
        member_id = CommonFunction.getFinalMemberId(request.user)
        group_ids = request.data.get("groupIds", [])
        if member_id > 0 and group_ids:
            Group.objects.filter(memberId=member_id, groupId__in=group_ids).delete()
            return CustomResponse(data=res_body, status=200, message="Group deleted successfully.")
        else:
            return CustomResponse(data=res_body, status=500, message="error")
    except Exception as e:
        logger.error(f"deleteBulkGroup error: {e}", exc_info=True)
        return CustomResponse(data=res_body, status=500, message="error")


@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_udf_list(request: Request, groupId: int) -> CustomResponse:
    """Returns mapped default and custom custom-field keys/labels."""
    try:
        final_list = []
        for k, v in zip(UDF_KEYS, UDF_VALUES):
            final_list.append({
                "key": k,
                "value": v
            })

        udfs = Udf.objects.filter(groupId=groupId).order_by('udfLabel')
        for u in udfs:
            final_list.append({
                "key": f"udf{u.udfLabel}",
                "value": u.udf
            })
        return CustomResponse(data=final_list, status=200, message="UDF list fetched successfully.")
    except Exception as e:
        logger.error(f"getGroupUDFList error: {e}", exc_info=True)
        return CustomResponse(data=None, status=500, message="error")


@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_udf_value_list(request: Request, groupId: int, groupUDF: str) -> CustomResponse:
    """Retrieves list of unique values for a chosen field, adhering to Java-mapped properties."""
    try:
        member_id = CommonFunction.getFinalMemberId(request.user)
        contacts = Userlist.objects.filter(
            groupId=groupId,
            memberId=member_id,
            status='Subscribed',
            badEmail='N',
            badPhoneNumber='N'
        ).filter(
            Q(smsStatus='Subscribed') | Q(smsStatus__isnull=True)
        ).filter(
            Q(optId__isnull=True) | Q(optId=0)
        ).order_by('firstName')

        udflist_value: Set[str] = set()
        for u in contacts:
            val = None
            if groupUDF == "First_Name":
                val = u.firstName
            elif groupUDF == "Last_Name":
                val = u.lastName
            elif groupUDF == "Email":
                val = u.emailDomain
            elif groupUDF == "phoneNumber":
                val = u.phoneNumber
            elif groupUDF == "streetAddress2":
                val = u.streetAddress2
            elif groupUDF == "streetAddress1":
                val = u.streetAddress1
            elif groupUDF == "city":
                val = u.city
            elif groupUDF == "stateProvRegion":
                val = u.status
            elif groupUDF == "zipPostalCode":
                val = u.zipPostalCode
            elif groupUDF == "region":
                val = u.region
            elif groupUDF == "gender":
                val = u.gender
            elif groupUDF == "age":
                val = str(u.age) if u.age is not None else None
            elif groupUDF == "contactRating":
                val = str(u.contactRating) if u.contactRating is not None else None
            elif groupUDF == "tags":
                val = u.tags

            if val is not None:
                udflist_value.add(val)

        return CustomResponse(data=list(udflist_value), status=200, message="UDF list value fetched successfully.")
    except Exception as e:
        logger.error(f"getGroupUDFValueList error: {e}", exc_info=True)
        return CustomResponse(data=None, status=500, message="error")


@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_group_contact_header(request: Request, groupId: int) -> CustomResponse:
    """Returns labels mapping dictionary for standard and custom keys."""
    try:
        res_body = {}
        for k, v in zip(CONTACT_HEADER_KEYS, CONTACT_HEADER_VALUES):
            res_body[k] = v

        udfs = Udf.objects.filter(groupId=groupId).order_by('udfLabel')
        for u in udfs:
            res_body[f"udf{u.udfLabel}"] = u.udf

        return CustomResponse(data=res_body, status=200, message="Header list fetched successfully.")
    except Exception as e:
        logger.error(f"getGroupContactHeader error: {e}", exc_info=True)
        return CustomResponse(data=None, status=500, message="error")


@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_group_contact_header_key(request: Request, groupId: int) -> CustomResponse:
    """Returns a list of header keys including standard and group custom keys."""
    try:
        keys = list(CONTACT_HEADER_KEYS)
        udfs = Udf.objects.filter(groupId=groupId).order_by('udfLabel')
        for u in udfs:
            keys.append(f"udf{u.udfLabel}")

        return CustomResponse(data=keys, status=200, message="Header list fetched successfully.")
    except Exception as e:
        logger.error(f"getGroupContactHeaderKey error: {e}", exc_info=True)
        return CustomResponse(data=None, status=500, message="error")


@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def invite_by_url(request: Request) -> CustomResponse:
    """Generates encrypted group invitation token string."""
    res_body: Dict[str, Any] = {}
    try:
        group_id = request.query_params.get("groupId")
        sub_member_id = request.query_params.get("subMemberId")
        if not group_id or not sub_member_id:
            return CustomResponse(data=None, status=400, message="groupId and subMemberId are required.")

        member_id = CommonFunction.getFinalMemberId(request.user)
        plain_text = f"{group_id}~{member_id}~{sub_member_id}"
        encrypted_str = DecryptString.setEncDecUser(plain_text, "", "Y")

        res_body["inviteByUrl"] = encrypted_str
        return CustomResponse(data=res_body, status=200, message="Data fetched successfully.")
    except Exception as e:
        logger.error(f"inviteByUrl error: {e}", exc_info=True)
        return CustomResponse(data=res_body, status=500, message="error")


@api_view(['POST'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_invite_by_url_data(request: Request) -> CustomResponse:
    """Decrypts invitation token and returns associated metadata."""
    res_body: Dict[str, Any] = {}
    try:
        q = request.data.get("q")
        if not q:
            return CustomResponse(data=None, status=400, message="q is required.")

        decrypted_str = DecryptString.setEncDecUser(q, "display", "Y")
        parts = decrypted_str.split("~")
        group_id = int(parts[0])
        member_id = int(parts[1])
        sub_member_id = int(parts[2])

        udfs = Udf.objects.filter(groupId=group_id).order_by('udfLabel')
        udfs_list = [{
            "id": u.id,
            "groupId": u.groupId,
            "udf": u.udf,
            "udfLabel": u.udfLabel
        } for u in udfs]

        res_body["memberId"] = member_id
        res_body["subMemberId"] = sub_member_id
        res_body["groupId"] = group_id
        res_body["udfs"] = udfs_list

        return CustomResponse(data=res_body, status=200, message="Data fetched successfully.")
    except Exception as e:
        logger.error(f"getInviteByUrlData error: {e}", exc_info=True)
        return CustomResponse(data=None, status=500, message="error")


@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_group_udf(request: Request, groupId: int) -> CustomResponse:
    """Returns custom UDF information for a group."""
    res_body: Dict[str, Any] = {}
    try:
        udfs = Udf.objects.filter(groupId=groupId).order_by('udfLabel')
        udfs_list = [{
            "id": u.id,
            "groupId": u.groupId,
            "udf": u.udf,
            "udfLabel": u.udfLabel
        } for u in udfs]

        res_body["groupId"] = groupId
        res_body["udfs"] = udfs_list

        return CustomResponse(data=res_body, status=200, message="UDF fetched successfully.")
    except Exception as e:
        logger.error(f"getGroupUDF error: {e}", exc_info=True)
        return CustomResponse(data=None, status=500, message="error")


@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_group_first_records(request: Request, groupId: int) -> CustomResponse:
    """Fetches first contact record's attributes and maps dynamic UDF keys."""
    res_body: Dict[str, Any] = {}
    try:
        member_id = CommonFunction.getFinalMemberId(request.user)
        userlist = Userlist.objects.filter(
            groupId=groupId,
            memberId=member_id,
            status='Subscribed',
            badEmail='N',
            badPhoneNumber='N'
        ).filter(
            Q(smsStatus='Subscribed') | Q(smsStatus__isnull=True)
        ).filter(
            Q(optId__isnull=True) | Q(optId=0)
        ).exclude(
            email__isnull=True
        ).exclude(
            email=''
        ).order_by('firstName').first()

        if userlist:
            res_body["First_Name"] = userlist.firstName or ""
            res_body["Last_Name"] = userlist.lastName or ""
            email_str = ""
            if userlist.email and userlist.email.strip():
                try:
                    email_str = DecryptString.setEncDecUser(userlist.email, "display", "Y") or ""
                except Exception:
                    email_str = ""
            res_body["Email"] = email_str
            res_body["Contact_No"] = userlist.phoneNumber or ""

            udfs = Udf.objects.filter(groupId=groupId).order_by('udfLabel')
            for udf in udfs:
                val = get_udf_val(userlist, udf.udfLabel)
                key = udf.udf.replace(" ", "_")
                if udf.udf == "birthday":
                    try:
                        val = DecryptString.setEncDecUser(val, "display", "Y") or ""
                    except Exception:
                        val = ""
                res_body[key] = val

        return CustomResponse(data=res_body, status=200, message="Fetched first record successfully.")
    except Exception as e:
        logger.error(f"getGroupFirstRecords error: {e}", exc_info=True)
        return CustomResponse(data=res_body, status=500, message="error")
