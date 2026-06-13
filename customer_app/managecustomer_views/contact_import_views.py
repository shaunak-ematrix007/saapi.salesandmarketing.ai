import logging
import os
import re
import csv
import random
from typing import Any, Dict, List, Optional

from django.conf import settings
from django.db.models import Q, Min, Max, F
from django.utils import timezone
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated

from auth_app.authentication import CustomJWTAuthentication
from common_app.models import TempUserlist, TempCronUserListTotal, Udf, Group
from common_app.responses import CustomResponse
from common_app.common_variable import CommonVariable

logger = logging.getLogger(__name__)

# Constants
PHONE_NUMBER_LIST = [
    "mobilenumber", "mobileno", "mobile", "mobilephone", "contactnumber",
    "contactno", "contact", "cellnumber", "cellno", "cell", "cellphone",
    "phonenumber", "phoneno", "phone", "phonehome"
]

EMAIL_LIST = ["emailaddressother", "emailaddress", "email"]

SELECTED_FIELDS = [
    "First Name", "Last Name", "Full Name", "Email", "Contact No", "Phone",
    "Language", "Gender", "Birthday", "Street Address1", "Street Address2",
    "City", "State", "Country", "Zip Code", "Date Added", "Opt In Date",
    "Date Last Modified", "Signup Source", "Contact Rating", "Opt In Ip Address",
    "Confirm Ip", "Confirm Data Time", "Opt Out Ip Address", "Latitude",
    "Longitude", "GMTOff", "DSTOff", "Timezone", "Region", "Notes", "Tags",
    "Email Client Used", "CC", "LEID", "EUID", "Age", "Job Title",
    "Email Permission Status -  Other", "Email Lists", "Add this field"
]

JAVA_TO_DJANGO_FIELDS = {
    "emailId": "emailId",
    "firstName": "firstName",
    "lastName": "lastName",
    "fullName": "fullName",
    "email": "email",
    "phoneNumber": "phoneNumber",
    "phone": "phone",
    "usDefaultLanguage": "usDefaultLanguage",
    "streetAddress1": "streetAddress1",
    "streetAddress2": "streetAddress2",
    "age": "age",
    "birthday": "birthday",
    "cc": "cc",
    "city": "city",
    "confirmDateTime": "confirmDateTime",
    "confirmIP": "confirmIP",
    "contactRating": "contactRating",
    "country": "country",
    "dateAdded": "dateAdded",
    "dateLastModified": "dateLastModified",
    "dstOff": "dstOff",
    "emailClientUsed": "emailClientUsed",
    "emailLists": "emailLists",
    "emailPermissionStatusOther": "emailPermissionStatusOther",
    "euid": "euid",
    "gender": "gender",
    "gmtOff": "gmtOff",
    "jobTitle": "jobTitle",
    "latitude": "latitude",
    "leid": "leid",
    "longitude": "longitude",
    "notes": "notes",
    "optDate": "optDate",
    "optInIPAddress": "optInIPAddress",
    "optOutIpAddress": "optOutIpAddress",
    "region": "region",
    "selectDateFormat": "selectDateFormat",
    "signupSource": "signupSource",
    "stateProvRegion": "stateProvRegion",
    "status": "status",
    "subMemberId": "subMemberId",
    "tags": "tags",
    "timeZone": "timeZone",
    "transId": "transId",
    "zipPostalCode": "zipPostalCode",
    "udf1": "udf1",
    "udf2": "udf2",
    "udf3": "udf3",
    "udf4": "udf4",
    "udf5": "udf5",
    "udf6": "udf6",
    "udf7": "udf7",
    "udf8": "udf8",
    "udf9": "udf9",
    "udf10": "udf10"
}


# Helper Functions
def random_generation() -> int:
    """Mimics the Java random generation for transId."""
    return (1 + random.randint(0, 1)) * 10000 + random.randint(0, 9999)


def excel_to_csv(file_path: str) -> Optional[str]:
    """Converts xlsx/xls Excel files into a standard CSV format."""
    ext = os.path.splitext(file_path)[1].lower()
    if ext not in ('.xlsx', '.xls'):
        return None
    
    csv_path = os.path.splitext(file_path)[0] + '.csv'
    
    import openpyxl
    import xlrd
    
    try:
        rows = []
        if ext == '.xlsx':
            wb = openpyxl.load_workbook(file_path, data_only=True)
            sheet = wb.active if wb.active else wb.worksheets[0]
            for r in sheet.iter_rows(values_only=True):
                row_vals = []
                for val in r:
                    if val is None:
                        row_vals.append("")
                    elif isinstance(val, bool):
                        row_vals.append(str(val))
                    elif isinstance(val, (int, float)):
                        if isinstance(val, float) and val.is_integer():
                            row_vals.append(str(int(val)))
                        else:
                            row_vals.append(str(val))
                    else:
                        row_vals.append(str(val))
                rows.append(row_vals)
        else:  # .xls
            wb = xlrd.open_workbook(file_path)
            sheet = wb.sheet_by_index(0)
            for r_idx in range(sheet.nrows):
                row_vals = []
                for c_idx in range(sheet.ncols):
                    cell = sheet.cell(r_idx, c_idx)
                    val = cell.value
                    if cell.ctype in (xlrd.XL_CELL_EMPTY, xlrd.XL_CELL_BLANK):
                        row_vals.append("")
                    elif cell.ctype == xlrd.XL_CELL_BOOLEAN:
                        row_vals.append(str(bool(val)))
                    elif cell.ctype == xlrd.XL_CELL_NUMBER:
                        row_vals.append(str(val))
                    else:
                        row_vals.append(str(val))
                rows.append(row_vals)
        
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(rows)
        return csv_path
    except Exception as e:
        logger.error(f"Error converting Excel to CSV: {e}", exc_info=True)
        raise e


def parse_and_insert_csv(file_path: str, data_headers: List[str], member_id: int, trans_id: str, date_format: str, with_header: bool) -> Dict[str, Any]:
    """Parses standard CSV and bulk inserts entries into tbl_temp_userlist."""
    field_mappings = []
    udf_counter = 0
    
    data_table_headers = {}
    data_table_udf = {}
    
    email_present = False
    phone_present = False
    
    for h in data_headers:
        if h == "firstname":
            field_mappings.append("firstName")
            data_table_headers["firstName"] = "First Name"
        elif h == "lastname":
            field_mappings.append("lastName")
            data_table_headers["lastName"] = "Last Name"
        elif h in EMAIL_LIST:
            field_mappings.append("email")
            email_present = True
            data_table_headers["email"] = "Email"
        elif h in PHONE_NUMBER_LIST:
            field_mappings.append("phoneNumber")
            phone_present = True
            data_table_headers["phoneNumber"] = "Phone Number"
        elif h == "gender":
            field_mappings.append("gender")
            data_table_headers["gender"] = "Gender"
        elif h in ("birthday", "dob"):
            field_mappings.append("birthday")
            data_table_headers["birthday"] = "Birthday"
        elif h == "streetaddress1":
            field_mappings.append("streetAddress1")
            data_table_headers["streetAddress1"] = "Street Address1"
        elif h == "streetaddress2":
            field_mappings.append("streetAddress2")
            data_table_headers["streetAddress2"] = "Street Address2"
        elif h == "city":
            field_mappings.append("city")
            data_table_headers["city"] = "City"
        elif h in ("state", "stateprovregion", "province"):
            field_mappings.append("stateProvRegion")
            data_table_headers["stateProvRegion"] = "State"
        elif h in ("zippostalcode", "zip", "zipcode", "postalcode"):
            field_mappings.append("zipPostalCode")
            data_table_headers["zipPostalCode"] = "Zipcode"
        elif h == "region":
            field_mappings.append("region")
            data_table_headers["region"] = "Region"
        elif h == "country":
            field_mappings.append("country")
            data_table_headers["country"] = "Country"
        elif h == "dateadded":
            field_mappings.append("dateAdded")
            data_table_headers["dateAdded"] = "Date Added"
        elif h == "datelastmodified":
            field_mappings.append("dateLastModified")
            data_table_headers["dateLastModified"] = "Date Added"
        elif h == "contactrating":
            field_mappings.append("contactRating")
            data_table_headers["contactRating"] = "Contact Rating"
        elif h == "optinipaddress":
            field_mappings.append("optInIPAddress")
            data_table_headers["optInIPAddress"] = "optInIPAddress"
        elif h == "optdate":
            field_mappings.append("optDate")
            data_table_headers["optDate"] = "optDate"
        elif h == "confirmip":
            field_mappings.append("confirmIP")
            data_table_headers["confirmIP"] = "confirmIP"
        elif h == "confirmdatetime":
            field_mappings.append("confirmDateTime")
            data_table_headers["confirmDateTime"] = "confirmDateTime"
        elif h == "optoutipaddress":
            field_mappings.append("optOutIpAddress")
            data_table_headers["optOutIpAddress"] = "optOutIpAddress"
        elif h == "latitude":
            field_mappings.append("latitude")
            data_table_headers["latitude"] = "Latitude"
        elif h == "longitude":
            field_mappings.append("longitude")
            data_table_headers["longitude"] = "Longitude"
        elif h == "gmtoff":
            field_mappings.append("gmtOff")
            data_table_headers["gmtOff"] = "GMT Off"
        elif h == "dstoff":
            field_mappings.append("dstOff")
            data_table_headers["dstOff"] = "DST Off"
        elif h == "timezone":
            field_mappings.append("timeZone")
            data_table_headers["timeZone"] = "Timezone"
        elif h == "notes":
            field_mappings.append("notes")
            data_table_headers["notes"] = "Notes"
        elif h == "tags":
            field_mappings.append("tags")
            data_table_headers["tags"] = "Tags"
        elif h == "cc":
            field_mappings.append("cc")
            data_table_headers["cc"] = "CC"
        elif h == "leid":
            field_mappings.append("leid")
            data_table_headers["leid"] = "LEID"
        elif h == "euid":
            field_mappings.append("euid")
            data_table_headers["euid"] = "EUID"
        elif h == "emailclientused":
            field_mappings.append("emailClientUsed")
            data_table_headers["emailClientUsed"] = "Email Client Used"
        elif h == "age":
            field_mappings.append("age")
            data_table_headers["age"] = "Age"
        elif h == "status":
            field_mappings.append("status")
            data_table_headers["status"] = "Status"
        elif h == "jobtitle":
            field_mappings.append("jobTitle")
            data_table_headers["jobTitle"] = "Job Title"
        elif h == "emailpermissionstatusother":
            field_mappings.append("emailPermissionStatusOther")
            data_table_headers["emailpermissionstatusother"] = "Email Permission Status Other"
        elif h == "emaillists":
            field_mappings.append("emailLists")
            data_table_headers["emailLists"] = "Email Lists"
        else:
            udf_counter += 1
            field_mappings.append(f"udf{udf_counter}")
            data_table_headers[f"udf{udf_counter}"] = h
            data_table_udf[f"udf{udf_counter}"] = h
            
    objects_to_create = []
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        reader = csv.reader(f)
        if with_header:
            next(reader, None)
            
        for row in reader:
            if not row:
                continue
            params = dict()
            params["memberId"] = member_id
            params["transId"] = trans_id
            params["selectDateFormat"] = date_format

            for idx, val in enumerate(row):
                if idx < len(field_mappings):
                    field_name = field_mappings[idx]
                    clean_val = val.strip() if val else ""
                    if field_name == "age":
                        try:
                            params[field_name] = float(clean_val) if clean_val else None
                        except ValueError:
                            params[field_name] = None
                    elif field_name == "contactRating":
                        try:
                            params[field_name] = int(clean_val) if clean_val else None
                        except ValueError:
                            params[field_name] = None
                    else:
                        params[field_name] = clean_val
            
            objects_to_create.append(TempUserlist(**params))
            
    if objects_to_create:
        TempUserlist.objects.bulk_create(objects_to_create)
        
    return {
        "email": email_present,
        "phoneNumber": phone_present,
        "dataTableHeaders": data_table_headers,
        "dataTableUdf": data_table_udf
    }


def serialize_temp_userlist(instance: TempUserlist) -> Dict[str, Any]:
    """Serializes a TempUserlist model to a dict, cleaning up None values."""
    raw_dict = {
        "emailId": instance.emailId,
        "age": instance.age,
        "birthday": instance.birthday,
        "cc": instance.cc,
        "city": instance.city,
        "confirmDateTime": instance.confirmDateTime,
        "confirmIP": instance.confirmIP,
        "contactRating": instance.contactRating,
        "country": instance.country,
        "dateAdded": instance.dateAdded,
        "dateLastModified": instance.dateLastModified,
        "dstOff": instance.dstOff,
        "email": instance.email,
        "emailClientUsed": instance.emailClientUsed,
        "emailLists": instance.emailLists,
        "emailPermissionStatusOther": instance.emailPermissionStatusOther,
        "euid": instance.euid,
        "firstName": instance.firstName,
        "gender": instance.gender,
        "gmtOff": instance.gmtOff,
        "jobTitle": instance.jobTitle,
        "lastName": instance.lastName,
        "latitude": instance.latitude,
        "leid": instance.leid,
        "longitude": instance.longitude,
        "notes": instance.notes,
        "optDate": instance.optDate,
        "optInIPAddress": instance.optInIPAddress,
        "optOutIpAddress": instance.optOutIpAddress,
        "phoneNumber": instance.phoneNumber,
        "region": instance.region,
        "selectDateFormat": instance.selectDateFormat,
        "signupSource": instance.signupSource,
        "stateProvRegion": instance.stateProvRegion,
        "status": instance.status,
        "streetAddress1": instance.streetAddress1,
        "streetAddress2": instance.streetAddress2,
        "fullName": instance.fullName,
        "phone": instance.phone,
        "subMemberId": instance.subMemberId,
        "tags": instance.tags,
        "timeZone": instance.timeZone,
        "transId": instance.transId,
        "udf1": instance.udf1,
        "udf2": instance.udf2,
        "udf3": instance.udf3,
        "udf4": instance.udf4,
        "udf5": instance.udf5,
        "udf6": instance.udf6,
        "udf7": instance.udf7,
        "udf8": instance.udf8,
        "udf9": instance.udf9,
        "udf10": instance.udf10,
        "zipPostalCode": instance.zipPostalCode,
        "memberId": instance.memberId,
        "usDefaultLanguage": instance.usDefaultLanguage
    }
    return {k: v for k, v in raw_dict.items() if v is not None}


# Staging Query Translators
def query_with_phonenumber_and_email(member_id: int, trans_id: str):
    invalid_email_regex = r'^[a-zA-Z0-9][+a-zA-Z0-9._-]*@[a-zA-Z0-9][a-zA-Z0-9._-]*[a-zA-Z0-9]*\.[a-zA-Z]{2,4}$'
    q_expr = (
        ~Q(email__regex=invalid_email_regex) |
        Q(email__contains=' ') |
        Q(phoneNumber='') |
        Q(phoneNumber__isnull=True) |
        Q(udf1='') | Q(udf2='') | Q(udf3='') | Q(udf4='') | Q(udf5='') |
        Q(udf6='') | Q(udf7='') | Q(udf8='') | Q(udf9='') | Q(udf10='')
    )
    return TempUserlist.objects.filter(memberId=member_id, transId=trans_id).filter(q_expr).order_by('emailId')


def query_without_phonenumber_and_email(member_id: int, trans_id: str):
    q_expr = (
        Q(udf1='') | Q(udf2='') | Q(udf3='') | Q(udf4='') | Q(udf5='') |
        Q(udf6='') | Q(udf7='') | Q(udf8='') | Q(udf9='') | Q(udf10='')
    )
    return TempUserlist.objects.filter(memberId=member_id, transId=trans_id).filter(q_expr)


def query_with_email(member_id: int, trans_id: str):
    invalid_email_regex = r'^[a-zA-Z0-9][+a-zA-Z0-9._-]*@[a-zA-Z0-9][a-zA-Z0-9._-]*[a-zA-Z0-9]*\.[a-zA-Z]{2,4}$'
    q_expr = (
        ~Q(email__regex=invalid_email_regex) |
        Q(email__contains=' ') |
        Q(udf1='') | Q(udf2='') | Q(udf3='') | Q(udf4='') | Q(udf5='') |
        Q(udf6='') | Q(udf7='') | Q(udf8='') | Q(udf9='') | Q(udf10='')
    )
    return TempUserlist.objects.filter(memberId=member_id, transId=trans_id).filter(q_expr).order_by('emailId')


def query_without_phonenumber(member_id: int, trans_id: str):
    q_expr = (
        Q(phoneNumber='') |
        Q(phoneNumber__isnull=True) |
        Q(udf1='') | Q(udf2='') | Q(udf3='') | Q(udf4='') | Q(udf5='') |
        Q(udf6='') | Q(udf7='') | Q(udf8='') | Q(udf9='') | Q(udf10='')
    )
    return TempUserlist.objects.filter(memberId=member_id, transId=trans_id).filter(q_expr).order_by('emailId')


def populate_import_contact_helper(file_path: str, member_id: int, trans_id: str, date_format: str, headers: List[str], with_header: bool, res_body: Dict[str, Any]) -> None:
    """Helper to parse CSV and populate response dict structure."""
    parse_result = parse_and_insert_csv(
        file_path=file_path,
        data_headers=headers,
        member_id=member_id,
        trans_id=trans_id,
        date_format=date_format,
        with_header=with_header
    )
    
    email_present = parse_result["email"]
    phone_present = parse_result["phoneNumber"]
    data_table_headers = parse_result["dataTableHeaders"]
    
    aggregate_res = TempUserlist.objects.filter(memberId=member_id, transId=trans_id).aggregate(
        minEmailId=Min('emailId'),
        maxEmailId=Max('emailId')
    )
    
    res_body["cronStartId"] = aggregate_res.get("minEmailId")
    res_body["cronEndId"] = aggregate_res.get("maxEmailId")
    
    if email_present and phone_present:
        qs = query_with_phonenumber_and_email(member_id, trans_id)
    elif not email_present and not phone_present:
        qs = query_without_phonenumber_and_email(member_id, trans_id)
    elif email_present:
        qs = query_with_email(member_id, trans_id)
    else:
        qs = query_without_phonenumber(member_id, trans_id)
        
    res_body["body"] = [serialize_temp_userlist(instance) for instance in qs]
    res_body["totalRecord"] = TempUserlist.objects.filter(memberId=member_id, transId=trans_id).count()
    
    invalid_email_regex_total = r'^[a-zA-Z0-9][+a-zA-Z0-9._-]*@[a-zA-Z0-9][a-zA-Z0-9._-]*[a-zA-Z0-9]*.[a-zA-Z]{2,4}$'
    invalid_count = TempUserlist.objects.filter(memberId=member_id, transId=trans_id).filter(
        ~Q(email__regex=invalid_email_regex_total)
    ).count()
    res_body["invalidEmails"] = invalid_count
    
    res_body["transId"] = trans_id
    res_body["dataTableHeaders"] = data_table_headers
    res_body["dataTableUdf"] = parse_result["dataTableUdf"]


def add_temp_cron_contact_logic(temp_cron: TempCronUserListTotal, udfs: Dict[str, str], trans_id: str) -> Dict[str, Any]:
    """Consolidated business logic for registering cron job custom fields (UDFs) and shifting columns."""
    res_body = {}
    
    udf_list = Udf.objects.filter(groupId=temp_cron.cronGroupId)
    existing_udf_names = [u.udf for u in udf_list]
    
    requested_udfs = list(udfs.values())
    request_udfs_label = list(udfs.keys())
    
    udf_set = set(requested_udfs)
    old_udf_set = set(existing_udf_names)
    old_udf_set.update(udf_set)
    
    total_udf_size = len(existing_udf_names)
    
    if len(udf_set) < len(requested_udfs):
        res_body["error"] = "Same udf is not allow."
        return res_body
    elif len(old_udf_set) > 10:
        res_body["error"] = "Custom field count is more then allowed limit."
        return res_body
        
    # Create missing Udfs
    for udf_string in requested_udfs:
        if udf_string not in existing_udf_names:
            total_udf_size += 1
            Udf.objects.create(
                udf=udf_string,
                groupId=temp_cron.cronGroupId,
                udfLabel=total_udf_size
            )
            
    # Blank fields query
    blank_fields = {}
    for i in range(1, 11):
        if str(i) not in request_udfs_label:
            blank_fields[f"udf{i}"] = ""
            
    if blank_fields:
        TempUserlist.objects.filter(
            memberId=CommonVariable.FINALMEMBERID,
            transId=trans_id
        ).update(**blank_fields)
        
    # Shifting logic
    move_list = {}
    for label_str, udf_name in udfs.items():
        try:
            udf_obj = Udf.objects.get(groupId=temp_cron.cronGroupId, udf=udf_name)
            move_list[udf_obj.udfLabel] = int(label_str)
        except Udf.DoesNotExist:
            logger.error(f"Udf {udf_name} not found for group {temp_cron.cronGroupId}")
            
    # Shift labels descendingly
    for i in range(10, 0, -1):
        target_src = move_list.get(i)
        if target_src is not None and target_src != i:
            TempUserlist.objects.filter(
                memberId=CommonVariable.FINALMEMBERID,
                transId=trans_id
            ).update(**{f"udf{i}": F(f"udf{target_src}")})
            
            TempUserlist.objects.filter(
                memberId=CommonVariable.FINALMEMBERID,
                transId=trans_id
            ).update(**{f"udf{target_src}": ""})
            
    temp_cron.cronProcess = "N"
    temp_cron.cronProcessFinished = "N"
    temp_cron.save()
    
    return res_body


def import_contact_by_admin_side_helper(import_contact_dto: Dict[str, Any]) -> Dict[str, Any]:
    """Helper implementing importContactByAdminSide logic."""
    member_id = import_contact_dto.get("memberId")
    group_name = import_contact_dto.get("groupName")
    file_path = import_contact_dto.get("path")
    date_format = import_contact_dto.get("format")
    
    # 1. Check if group exists else create new
    exists = Group.objects.filter(memberId=member_id, groupName=group_name).exists()
    if not exists:
        group = Group.objects.create(
            memberId=member_id,
            groupName=group_name,
            dateRegistered=timezone.now()
        )
        cron_group_id = group.groupId
    else:
        group = Group.objects.filter(memberId=member_id, groupName=group_name).first()
        cron_group_id = group.groupId
        
    csv_path = excel_to_csv(file_path)
    if csv_path:
        if os.path.exists(file_path):
            os.remove(file_path)
        file_path = csv_path
        
    trans_id = str(random_generation())
    
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        first_line = f.readline()
    cleaned_line = first_line.replace(',,', ', ,') if first_line else ""
    raw_headers = cleaned_line.strip('\r\n').split(',') if cleaned_line else []
    headers = []
    for h in raw_headers:
        cleaned = re.sub(r'[-+.\^:,_]', '', h.lower().strip().replace(' ', ''))
        headers.append(cleaned)
        
    phone_email_header = False
    for header in headers:
        if header in PHONE_NUMBER_LIST or header in EMAIL_LIST:
            phone_email_header = True
            break
            
    res_body = {}
    res_body_pc = {}
    with_header = True
    
    column_headers = import_contact_dto.get("columnHeaders")
    if column_headers is not None:
        non_headers = []
        phone_email = False
        for entry_val in column_headers.values():
            cleaned = re.sub(r'[-+.\^:,_]', '', entry_val.lower().strip().replace(' ', ''))
            non_headers.append(cleaned)
            
        unique_non_headers = set(non_headers)
        for header in non_headers:
            if header in PHONE_NUMBER_LIST or header in EMAIL_LIST:
                phone_email = True
                break
                
        if "" in non_headers:
            res_body["error"] = "Please select field."
            return res_body
        elif len(unique_non_headers) < len(non_headers):
            res_body["error"] = "Same header name is not allow."
            return res_body
        elif "firstname" not in non_headers:
            res_body["error"] = "Please select first name."
            return res_body
        elif "lastname" not in non_headers:
            res_body["error"] = "Please select last name."
            return res_body
        elif not phone_email:
            res_body["error"] = "Please enter email address / mobile number."
            return res_body
        else:
            with_header = False
            populate_import_contact_helper(
                file_path=file_path,
                member_id=int(member_id),
                trans_id=trans_id,
                date_format=date_format,
                headers=non_headers,
                with_header=with_header,
                res_body=res_body_pc
            )
    elif "firstname" in headers or "lastname" in headers or phone_email_header:
        populate_import_contact_helper(
            file_path=file_path,
            member_id=int(member_id),
            trans_id=trans_id,
            date_format=date_format,
            headers=headers,
            with_header=with_header,
            res_body=res_body_pc
        )
    else:
        select_headers = {}
        for i, h in enumerate(raw_headers):
            select_headers[str(i + 1)] = h.strip()
        res_body["headers"] = SELECTED_FIELDS
        res_body["body"] = select_headers
        return res_body

    if "error" in res_body_pc:
        return res_body_pc
        
    temp_cron = TempCronUserListTotal(
        cronMemberId=member_id,
        cronGroupId=cron_group_id,
        cronStartId=res_body_pc.get("cronStartId"),
        cronEndId=res_body_pc.get("cronEndId"),
        cronProcess="N",
        cronProcessFinished="N"
    )
    
    udfs = res_body_pc.get("dataTableUdf", {})
    return add_temp_cron_contact_logic(temp_cron, udfs, trans_id)


# API Views
@api_view(['POST'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def import_contact(request: Request) -> CustomResponse:
    """Stages contacts from a file upload, handling formats like XLS, XLSX, and CSV."""
    res_body: Dict[str, Any] = {}
    data = request.data
    
    date_format = data.get("format")
    file_path = data.get("path")
    member_id = data.get("memberId")
    column_headers = data.get("columnHeaders")
    
    if not date_format:
        return CustomResponse(data=res_body, status=400, message="Please select date format.")

    if not file_path:
        return CustomResponse(data=res_body, status=400, message="Path is required.")

    if not member_id:
        return CustomResponse(data=res_body, status=400, message="Member ID is required.")

    try:
        csv_path = excel_to_csv(file_path)
        if csv_path:
            if os.path.exists(file_path):
                os.remove(file_path)
            file_path = csv_path
    except Exception as e:
        logger.error(f"Excel conversion failed: {e}", exc_info=True)
        return CustomResponse(data=res_body, status=500, message="Internal Server Error")

    trans_id = str(random_generation())
    
    try:
        if not os.path.exists(file_path):
            return CustomResponse(data=res_body, status=500, message="File not found")
            
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            first_line = f.readline()
            
        cleaned_line = first_line.replace(',,', ', ,') if first_line else ""
        raw_headers = cleaned_line.strip('\r\n').split(',') if cleaned_line else []
        headers = []
        for h in raw_headers:
            cleaned = re.sub(r'[-+.\^:,_]', '', h.lower().strip().replace(' ', ''))
            headers.append(cleaned)
            
        phone_email_header = False
        for header in headers:
            if header in PHONE_NUMBER_LIST or header in EMAIL_LIST:
                phone_email_header = True
                break
                
        with_header = True
        
        if column_headers is not None:
            non_headers = []
            phone_email = False
            for entry_val in column_headers.values():
                cleaned = re.sub(r'[-+.\^:,_]', '', entry_val.lower().strip().replace(' ', ''))
                non_headers.append(cleaned)
                
            unique_non_headers = set(non_headers)
            for header in non_headers:
                if header in PHONE_NUMBER_LIST or header in EMAIL_LIST:
                    phone_email = True
                    break
                    
            if "" in non_headers:
                res_body["error"] = "Please select field."
            elif len(unique_non_headers) < len(non_headers):
                res_body["error"] = "Same header name is not allow."
            elif "firstname" not in non_headers:
                res_body["error"] = "Please select first name."
            elif "lastname" not in non_headers:
                res_body["error"] = "Please select last name."
            elif not phone_email:
                res_body["error"] = "Please enter email address / mobile number."
            else:
                has_firstname = "firstname" in non_headers
                has_lastname = "lastname" in non_headers
                has_email = any(h in EMAIL_LIST for h in non_headers)
                has_phone = any(h in PHONE_NUMBER_LIST for h in non_headers)
                
                if has_firstname and has_lastname and (has_email or has_phone):
                    with_header = False
                    populate_import_contact_helper(
                        file_path=file_path,
                        member_id=int(member_id),
                        trans_id=trans_id,
                        date_format=date_format,
                        headers=non_headers,
                        with_header=with_header,
                        res_body=res_body
                    )
                else:
                    res_body["error"] = "Invalid file format. Please download sample file and reference structure."
        elif "firstname" in headers or "lastname" in headers or phone_email_header:
            has_firstname = "firstname" in headers
            has_lastname = "lastname" in headers
            has_email = any(h in EMAIL_LIST for h in headers)
            has_phone = any(h in PHONE_NUMBER_LIST for h in headers)
            
            if has_firstname and has_lastname and (has_email or has_phone):
                populate_import_contact_helper(
                    file_path=file_path,
                    member_id=int(member_id),
                    trans_id=trans_id,
                    date_format=date_format,
                    headers=headers,
                    with_header=with_header,
                    res_body=res_body
                )
            else:
                res_body["error"] = "Invalid file format. Please download sample file and reference structure."
        else:
            select_headers = {}
            for i, h in enumerate(raw_headers):
                select_headers[str(i + 1)] = h.strip()
            res_body["headers"] = SELECTED_FIELDS
            res_body["body"] = select_headers
            
    except Exception as e:
        logger.error(f"importContact error: {e}", exc_info=True)
        return CustomResponse(data=res_body, status=500, message="Internal Server Error")

    if "error" in res_body:
        message = res_body["error"]
        del res_body["error"]
        return CustomResponse(data=res_body, status=244, message=message)  # 204 status mapped correctly
        
    return CustomResponse(data=res_body, status=200, message="File import successfully.")


@api_view(['POST'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_header_field_mapping(request: Request) -> CustomResponse:
    """Returns mapped columns against existing custom fields (UDFs) for CSV/Excel file parsing."""
    res_body: List[Dict[str, Any]] = []
    data = request.data
    
    path = data.get("path")
    group_id = data.get("groupId")
    column_headers = data.get("columnHeaders")
    quickbook = data.get("quickbook", "")
    salesforce = data.get("salesforce", "")
    trans_id = data.get("transId")
    
    if not path and not (quickbook.lower() == "yes" or salesforce.lower() == "yes"):
        return CustomResponse(data=res_body, status=400, message="Path is required unless quickbook or salesforce is yes")
        
    if not group_id:
        return CustomResponse(data=res_body, status=400, message="groupId is required")
        
    try:
        if path:
            csv_path = excel_to_csv(path)
            if csv_path:
                path = csv_path
                
        udfs = Udf.objects.filter(groupId=group_id)
        udf_list = [u.udf for u in udfs]
        udf_list.append("Add This Field")
        udf_list.append("Do Not Add This Field")
        
        if quickbook.lower() == "yes" or salesforce.lower() == "yes":
            temp_userlist = TempUserlist.objects.filter(transId=trans_id).first()
            if temp_userlist:
                res_body.append({"key": "First Name", "value": ["First Name"], "eg": temp_userlist.firstName or ""})
                res_body.append({"key": "Last Name", "value": ["Last Name"], "eg": temp_userlist.lastName or ""})
                res_body.append({"key": "Email", "value": ["Email"], "eg": temp_userlist.email or ""})
                res_body.append({"key": "Mobile Number", "value": ["Mobile Number"], "eg": temp_userlist.phoneNumber or ""})
                res_body.append({"key": "Street Address1", "value": ["Street Address1"], "eg": temp_userlist.streetAddress1 or ""})
                res_body.append({"key": "Street Address2", "value": ["Street Address2"], "eg": temp_userlist.streetAddress2 or ""})
                res_body.append({"key": "City", "value": ["City"], "eg": temp_userlist.city or ""})
                res_body.append({"key": "Country", "value": ["Country"], "eg": temp_userlist.country or ""})
                res_body.append({"key": "Zip Code", "value": ["Zip Code"], "eg": temp_userlist.zipPostalCode or ""})
                res_body.append({"key": "Latitude", "value": ["Latitude"], "eg": temp_userlist.latitude or ""})
                res_body.append({"key": "Longitude", "value": ["Longitude"], "eg": temp_userlist.longitude or ""})
                res_body.append({"key": "Notes", "value": ["Notes"], "eg": temp_userlist.notes or ""})
                
                if quickbook.lower() == "yes":
                    res_body.append({"key": "Tags", "value": ["Tags"], "eg": temp_userlist.tags or ""})
                    res_body.append({"key": "Job Title", "value": ["Job Title"], "eg": temp_userlist.jobTitle or ""})
        else:
            lines = []
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                reader = csv.reader(f)
                for row in reader:
                    lines.append(row)
                    
            if not lines:
                return CustomResponse(data=res_body, status=400, message="File is empty")
                
            headers = []
            headers_display = []
            eg = []
            
            if column_headers is not None:
                for h in column_headers:
                    cleaned = re.sub(r'[-+.\^:,_]', '', h.lower().strip().replace(' ', ''))
                    headers.append(cleaned)
                    headers_display.append(h)
                
                example_row = lines[1] if len(lines) > 1 else []
                for val in example_row:
                    eg.append(val)
            else:
                first_row = lines[0]
                for val in first_row:
                    cleaned = re.sub(r'[-+.\^:,_]', '', val.lower().strip().replace(' ', ''))
                    headers.append(cleaned)
                    headers_display.append(val)
                    
                example_row = lines[1] if len(lines) > 1 else []
                for val in example_row:
                    eg.append(val)
                    
            for i in range(len(headers)):
                h_cleaned = headers[i]
                h_display = headers_display[i]
                eg_val = eg[i] if i < len(eg) else ""
                
                if "firstname" in h_cleaned:
                    res_body.append({"key": h_display, "value": ["First Name"], "eg": eg_val})
                elif "lastname" in h_cleaned:
                    res_body.append({"key": h_display, "value": ["Last Name"], "eg": eg_val})
                elif h_cleaned in EMAIL_LIST:
                    res_body.append({"key": h_display, "value": ["Email"], "eg": eg_val})
                elif h_cleaned in PHONE_NUMBER_LIST:
                    res_body.append({"key": h_display, "value": ["Mobile Number"], "eg": eg_val})
                elif "gender" in h_cleaned:
                    res_body.append({"key": h_display, "value": ["Gender"], "eg": eg_val})
                elif "birthday" in h_cleaned or "dob" in h_cleaned:
                    res_body.append({"key": h_display, "value": ["Birthday"], "eg": eg_val})
                elif "streetaddress1" in h_cleaned:
                    res_body.append({"key": h_display, "value": ["Street Address1"], "eg": eg_val})
                elif "streetaddress2" in h_cleaned:
                    res_body.append({"key": h_display, "value": ["Street Address2"], "eg": eg_val})
                elif "city" in h_cleaned:
                    res_body.append({"key": h_display, "value": ["City"], "eg": eg_val})
                elif "state" in h_cleaned or "stateprovregion" in h_cleaned or "province" in h_cleaned:
                    res_body.append({"key": h_display, "value": ["State Proven Region"], "eg": eg_val})
                elif "zip" in h_cleaned or "zipcode" in h_cleaned or "postalcode" in h_cleaned:
                    res_body.append({"key": h_display, "value": ["Zip Code"], "eg": eg_val})
                elif "region" in h_cleaned:
                    res_body.append({"key": h_display, "value": ["Region"], "eg": eg_val})
                elif "country" in h_cleaned:
                    res_body.append({"key": h_display, "value": ["Country"], "eg": eg_val})
                elif "dateadded" in h_cleaned:
                    res_body.append({"key": h_display, "value": ["Date Added"], "eg": eg_val})
                elif "datelastmodified" in h_cleaned:
                    res_body.append({"key": h_display, "value": ["Last Date Modified"], "eg": eg_val})
                elif "contactrating" in h_cleaned:
                    res_body.append({"key": h_display, "value": ["Contact Rating"], "eg": eg_val})
                elif "optinipaddress" in h_cleaned:
                    res_body.append({"key": h_display, "value": ["Opt In Ip Address"], "eg": eg_val})
                elif "optdate" in h_cleaned:
                    res_body.append({"key": h_display, "value": ["Opt In Date"], "eg": eg_val})
                elif "confirmip" in h_cleaned:
                    res_body.append({"key": h_display, "value": ["Confirm Ip"], "eg": eg_val})
                elif "confirmdatetime" in h_cleaned:
                    res_body.append({"key": h_display, "value": ["Confirm Date Time"], "eg": eg_val})
                elif "optoutipaddress" in h_cleaned:
                    res_body.append({"key": h_display, "value": ["Opt out Ip Address"], "eg": eg_val})
                elif "latitude" in h_cleaned:
                    res_body.append({"key": h_display, "value": ["Latitude"], "eg": eg_val})
                elif "longitude" in h_cleaned:
                    res_body.append({"key": h_display, "value": ["Longitude"], "eg": eg_val})
                elif "gmtoff" in h_cleaned:
                    res_body.append({"key": h_display, "value": ["GMTOff"], "eg": eg_val})
                elif "dstoff" in h_cleaned:
                    res_body.append({"key": h_display, "value": ["DSTOff"], "eg": eg_val})
                elif "timezone" in h_cleaned:
                    res_body.append({"key": h_display, "value": ["Timezone"], "eg": eg_val})
                elif "notes" in h_cleaned:
                    res_body.append({"key": h_display, "value": ["Notes"], "eg": eg_val})
                elif "tags" in h_cleaned:
                    res_body.append({"key": h_display, "value": ["Tags"], "eg": eg_val})
                elif "cc" in h_cleaned:
                    res_body.append({"key": h_display, "value": ["CC"], "eg": eg_val})
                elif "leid" in h_cleaned:
                    res_body.append({"key": h_display, "value": ["LEID"], "eg": eg_val})
                elif "euid" in h_cleaned:
                    res_body.append({"key": h_display, "value": ["EUID"], "eg": eg_val})
                elif "emailclientused" in h_cleaned:
                    res_body.append({"key": h_display, "value": ["Email Client Used"], "eg": eg_val})
                elif "age" in h_cleaned:
                    res_body.append({"key": h_display, "value": ["Age"], "eg": eg_val})
                elif "status" in h_cleaned:
                    res_body.append({"key": h_display, "value": ["Status"], "eg": eg_val})
                elif "jobtitle" in h_cleaned:
                    res_body.append({"key": h_display, "value": ["Job Title"], "eg": eg_val})
                elif "emailpermissionstatusother" in h_cleaned:
                    res_body.append({"key": h_display, "value": ["Email Permission Status - Other"], "eg": eg_val})
                elif "emaillists" in h_cleaned:
                    res_body.append({"key": h_display, "value": ["Email Lists"], "eg": eg_val})
                else:
                    if eg_val.strip():
                        res_body.append({"key": h_display, "value": udf_list, "eg": eg_val})
                        
        return CustomResponse(data=res_body, status=200, message="Contact mapping fetched successfully.")
    except Exception as e:
        logger.error(f"getHeaderFieldMapping error: {e}", exc_info=True)
        return CustomResponse(data=[], status=500, message="Exception while fetching columns Mapping")


@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_selected_headers(request: Request) -> CustomResponse:
    """Returns the static allowed select headers array."""
    return CustomResponse(data=SELECTED_FIELDS, status=200, message="Contact mapping fetched successfully.")


@api_view(['POST'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def add_temp_cron_contact(request: Request) -> CustomResponse:
    """Stages the staging records to final cron table and aligns custom field labels."""
    res_body: Dict[str, Any] = {}
    data = request.data
    
    cron_member_id = data.get("cronMemberId")
    cron_group_id = data.get("cronGroupId")
    cron_start_id = data.get("cronStartId")
    cron_end_id = data.get("cronEndId")
    cron_opt_in_message = data.get("cronOptInMessage")
    udfs = data.get("udfs", {})
    trans_id = data.get("transId")
    
    if not cron_member_id or not cron_group_id:
        return CustomResponse(data=res_body, status=400, message="cronMemberId and cronGroupId are required.")
        
    temp_cron = TempCronUserListTotal(
        cronMemberId=cron_member_id,
        cronGroupId=cron_group_id,
        cronStartId=cron_start_id,
        cronEndId=cron_end_id,
        cronOptInMessage=cron_opt_in_message
    )
    
    try:
        res_body = add_temp_cron_contact_logic(temp_cron, udfs, trans_id)
    except Exception as e:
        logger.error(f"addTempCronContact error: {e}", exc_info=True)
        return CustomResponse(data={}, status=500, message="Internal Server Error")
        
    message = "We have successfully staged your contacts.\nFor your safety, some data will be encrypted and tokenized. This process will take some time.\nPlease check back in with us and you will see an acknowledgement the process was successful."
    if "error" in res_body:
        message = res_body["error"]
        return CustomResponse(data={}, status=204, message=message)
        
    return CustomResponse(data=res_body, status=200, message=message)


@api_view(['POST'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def update_import_contact(request: Request) -> CustomResponse:
    """Updates custom or system fields of a contact in staging database."""
    res_body: Dict[str, Any] = {}
    data = request.data
    
    email_id = data.get("emailId")
    key = data.get("key")
    value = data.get("value")
    
    if not email_id or not key:
        return CustomResponse(data=res_body, status=400, message="emailId and key are required.")
        
    field_name = JAVA_TO_DJANGO_FIELDS.get(key)
    if not field_name:
        res_body["error"] = "Update failed due to invalid field key."
        return CustomResponse(data=res_body, status=204, message="Update failed due to invalid field key.")
        
    try:
        val = value
        if field_name == "age":
            try:
                val = float(val) if val else None
            except ValueError:
                val = None
        elif field_name == "contactRating":
            try:
                val = int(val) if val else None
            except ValueError:
                val = None
                
        TempUserlist.objects.filter(
            memberId=CommonVariable.FINALMEMBERID,
            emailId=email_id
        ).update(**{field_name: val})
        
    except Exception as e:
        logger.error(f"updateImportContact error: {e}", exc_info=True)
        res_body["error"] = "Internal Server Error"
        return CustomResponse(data=res_body, status=204, message="Internal Server Error")
        
    return CustomResponse(data=res_body, status=200, message="Update contact successfully.")


@api_view(['POST'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def import_contact_file(request: Request) -> CustomResponse:
    """Handles multipart file upload of Excel/CSV contact list."""
    res_body: Dict[str, Any] = {}
    file_obj = request.FILES.get('file')
    if not file_obj:
        return CustomResponse(data=res_body, status=500, message="Request must contains file")
        
    try:
        os.makedirs(settings.CSVSTORE_UPLOAD_DIR, exist_ok=True)
    except Exception as e:
        logger.error(f"Failed to create CSVSTORE_UPLOAD_DIR: {e}")
        pass

    file_path = os.path.join(settings.CSVSTORE_UPLOAD_DIR, file_obj.name)
    try:
        with open(file_path, 'wb+') as destination:
            for chunk in file_obj.chunks():
                destination.write(chunk)
                
        res_body["filePath"] = os.path.abspath(file_path)
        return CustomResponse(data=res_body, status=200, message="The File Uploaded Successfully")
    except Exception as e:
        logger.error(f"File upload error: {e}", exc_info=True)
        return CustomResponse(data=res_body, status=500, message=str(e))


@api_view(['POST'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def import_contact_by_admin_side(request: Request) -> CustomResponse:
    """Exposes importContactByAdminSide as a REST endpoint matching CustomerController mapping."""
    res_body: Dict[str, Any] = {}
    try:
        res_body = import_contact_by_admin_side_helper(request.data)
    except Exception as e:
        logger.error(f"importContactByAdminSide error : {e}", exc_info=True)
        return CustomResponse(data={}, status=500, message="Internal Server Error")
        
    message = "File import successfully."
    if "error" in res_body:
        message = res_body["error"]
        del res_body["error"]
        return CustomResponse(data=res_body, status=204, message=message)
        
    return CustomResponse(data=res_body, status=200, message=message)
