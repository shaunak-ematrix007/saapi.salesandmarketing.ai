import logging
import math
import csv
import os
from pathlib import Path
from typing import Any, Dict, Optional
from datetime import datetime
from django.utils import timezone
from django.db import transaction
from django.db.models import Q
from django.conf import settings
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated

from auth_app.authentication import CustomJWTAuthentication
from common_app.models import (
    Tenants, TenantDetails, Userlist, Plan, CountrySetting, Country,
    MemberStatus, TenDLCLogs, TenDLCRenew, TenDLCData,
    PlanLogs, CampaignTransaction
)
from common_app.responses import CustomResponse
from common_app.common_function import CommonFunction, send_email, MailRequestDTO
from common_app.decrypt_string import DecryptString

logger = logging.getLogger(__name__)


def serialize_member_dto(tenant: Tenants) -> Dict[str, Any]:
    """Helper to serialize Tenant properties for list views matching MemberDto.java contract."""
    email = tenant.ten_email
    first_name = DecryptString.setEncDecUser(tenant.ten_first_name, "display", "Y") or ""
    last_name = DecryptString.setEncDecUser(tenant.ten_last_name, "display", "Y") or ""
    cell = DecryptString.setEncDecUser(tenant.ten_cell_phone, "display", "Y") or ""
    
    member_type = "SubUser" if tenant.ten_parent_id and tenant.ten_parent_id > 0 else "User"
    
    status_val = ""
    if tenant.ten_status == 0:
        status_val = "Active"
    elif tenant.ten_status == 1:
        status_val = "Inactive"
    elif tenant.ten_status == 2:
        status_val = "Bad Credit Card"
    elif tenant.ten_status == 3:
        status_val = "Suspended"
        
    plan_name = ""
    details = getattr(tenant, 'details', None)
    if details and details.td_plan_id:
        try:
            plan_id = int(details.td_plan_id)
            if plan_id > 0:
                plan = Plan.objects.filter(planId=plan_id).first()
                if plan:
                    plan_name = plan.planName
        except ValueError:
            pass
            
    username = DecryptString.setEncDecUser(tenant.ten_username, "display", "Y") or ""
    
    return {
        "memberId": tenant.ten_id,
        "email": email,
        "firstName": first_name,
        "lastName": last_name,
        "cell": cell,
        "memberType": member_type,
        "memberStatusValue": status_val,
        "billDate": str(details.td_bill_date) if details and details.td_bill_date else None,
        "lastLoggedin": str(tenant.ten_last_logon) if tenant.ten_last_logon else None,
        "planName": plan_name,
        "username": username,
        "loginPreference": details.td_login_preference if details else None
    }


def serialize_member_full(tenant: Tenants) -> Dict[str, Any]:
    """Helper to serialize Tenant properties for detailed views matching MemberDto.java contract."""
    details = getattr(tenant, 'details', None)
    
    return {
        "memberId": tenant.ten_id,
        "membershipType": details.td_membership_type if details else "",
        "password": DecryptString.setEncDecUser(details.td_password if details else "", "display", "Y") or "",
        "companyName": "", 
        "firstName": DecryptString.setEncDecUser(tenant.ten_first_name, "display", "Y") or "",
        "lastName": DecryptString.setEncDecUser(tenant.ten_last_name, "display", "Y") or "",
        "memberFullName": f"{DecryptString.setEncDecUser(tenant.ten_first_name, 'display', 'Y') or ''} {DecryptString.setEncDecUser(tenant.ten_last_name, 'display', 'Y') or ''}".strip(),
        "address": DecryptString.setEncDecUser(tenant.ten_street_address1, "display", "Y") or "",
        "streetAddress": DecryptString.setEncDecUser(tenant.ten_street_address2, "display", "Y") or "",
        "city": DecryptString.setEncDecUser(tenant.ten_city, "display", "Y") or "",
        "state": DecryptString.setEncDecUser(tenant.ten_state, "display", "Y") or "",
        "postCode": DecryptString.setEncDecUser(tenant.ten_post_code, "display", "Y") or "",
        "country": tenant.ten_country if tenant.ten_country is not None else "",
        "phone": DecryptString.setEncDecUser(tenant.ten_phone, "display", "Y") or "",
        "fax": "", 
        "cell": DecryptString.setEncDecUser(tenant.ten_cell_phone, "display", "Y") or "",
        "email": DecryptString.setEncDecUser(tenant.ten_email, "display", "Y") or "",
        "memberStatus": tenant.ten_status,
        "businessName": "",
        "websiteName": "",
        "newsletterSubscribe": details.td_newsletter_subscribe if details else None,
        "is2FA": details.td_is2fa if details else 0,
        "dateRegistered": str(tenant.ten_date_registered) if tenant.ten_date_registered else None,
        "lastLoggedin": str(tenant.ten_last_logon) if tenant.ten_last_logon else None,
        "authorizeCustomerPaymentProfileId": DecryptString.setEncDecUser(details.td_authorize_customer_payment_profile_id if details else "", "display", "Y") or "",
        "authorizeCustomerProfileId": DecryptString.setEncDecUser(details.td_authorize_customer_profile_id if details else "", "display", "Y") or "",
        "billDate": str(details.td_bill_date) if details and details.td_bill_date else None,
        "memberDefaultLanguage": tenant.ten_default_language,
        "optin": details.td_opt_in if details else None,
        "parentMemberId": tenant.ten_parent_id,
        "secAns1": DecryptString.setEncDecUser(details.td_sec_ans_1 if details else "", "display", "Y") or "",
        "secAns2": DecryptString.setEncDecUser(details.td_sec_ans_2 if details else "", "display", "Y") or "",
        "secAns3": DecryptString.setEncDecUser(details.td_sec_ans_3 if details else "", "display", "Y") or "",
        "secQus1": details.td_sec_qus_1 if details else 0,
        "secQus2": details.td_sec_qus_2 if details else 0,
        "secQus3": details.td_sec_qus_3 if details else 0,
        "subaccountTypeId": details.td_sub_account_type_id if details else 0,
        "otp": details.td_otp if details else None,
        "planId": int(details.td_plan_id) if details and details.td_plan_id and details.td_plan_id.isdigit() else 0,
        "authKey": details.td_auth_key if details else "",
        "authToken": details.td_auth_token if details else "",
        "enableApi": details.td_enable_api if details else "N",
        "username": DecryptString.setEncDecUser(tenant.ten_username, "display", "Y") or "",
        "loginPreference": details.td_login_preference if details else ""
    }


def serialize_ten_dlc_data(data: TenDLCData) -> Dict[str, Any]:
    """Helper to serialize TenDLCData properties matching TenDLCDataDto.java contract."""
    reg_date_str = None
    if data.datRegistrationDate:
        try:
            reg_date_str = CommonFunction.displayDate(str(data.datRegistrationDate))
        except Exception:
            pass
    return {
        "datId": data.datId,
        "datMemberId": data.datMemberId,
        "datBrandName": data.datBrandName,
        "datCampaignType": data.datCampaignType,
        "datIsActive": data.datIsActive,
        "datRegistrationDate": reg_date_str
    }


def parse_dto_date(date_str: Optional[str]) -> Optional[str]:
    """Parses date string of MM/dd/yyyy format or returning standard YYYY-MM-DD format."""
    if not date_str:
        return None
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return date_str
    except ValueError:
        try:
            return CommonFunction.dbDate(date_str)
        except Exception:
            return None


@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_member_list_page(request: Request) -> CustomResponse:
    """
    Returns a paginated list of members, optionally filtered by name or email.
    """
    res_body: Dict[str, Any] = {}
    try:
        search_key = request.query_params.get("searchKey", "")
        page = int(request.query_params.get("page", 0))
        size = int(request.query_params.get("size", 10))

        offset = page * size
        limit = offset + size

        queryset = Tenants.objects.select_related('details').all().order_by('ten_id')

        if search_key:
            search_key_enc = DecryptString.setEncDecUser(search_key, "", "Y")
            queryset = queryset.filter(
                Q(ten_first_name__icontains=search_key_enc) |
                Q(ten_last_name__icontains=search_key_enc) |
                Q(ten_email__icontains=search_key_enc)
            )

        total_records = Tenants.objects.count()
        filtered_count = queryset.count()
        total_pages = math.ceil(filtered_count / size) if size > 0 else 0

        paginated_members = queryset[offset:limit]
        member_dtos = [serialize_member_dto(m) for m in paginated_members]

        res_body["getTotalPages"] = total_pages
        res_body["getNumber"] = page
        res_body["getSize"] = size
        res_body["memberList"] = member_dtos
        res_body["getTotalRecords"] = total_records

        return CustomResponse(data=res_body, status=200, message="Member List fetched successfully")
    except Exception as e:
        logger.error(f"get_member_list_page error: {e}", exc_info=True)
        return CustomResponse(data=res_body, status=500, message="error")


@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_member_by_id(request: Request, memberId: int) -> CustomResponse:
    """
    Returns full details for a member and their associated TenDLCData records.
    """
    res_body: Dict[str, Any] = {}
    try:
        tenant = Tenants.objects.select_related('details').filter(ten_id=memberId).first()
        if tenant:
            res_body["member"] = serialize_member_full(tenant)
            
            ten_dlc_dtos = []
            try:
                ten_dlc_list = TenDLCData.objects.filter(datMemberId=memberId)
                for td in ten_dlc_list:
                    ten_dlc_dtos.append(serialize_ten_dlc_data(td))
            except Exception as e:
                logger.error(f"Error fetching TenDLCData for member {memberId}: {e}")
                
            res_body["tenDLCData"] = ten_dlc_dtos
            return CustomResponse(data=res_body, status=200, message="Member fetched successfully")
        else:
            return CustomResponse(data=res_body, status=500, message="Member not found ")
    except Exception as e:
        logger.error(f"get_member_by_id error: {e}", exc_info=True)
        return CustomResponse(data=res_body, status=500, message="Member not found ")


@api_view(['DELETE'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_members(request: Request) -> CustomResponse:
    """
    Hard deletes list of member records by their IDs.
    """
    res_body: Dict[str, Any] = {}
    try:
        member_ids = request.data.get("memberIds", [])
        for mid in member_ids:
            if Tenants.objects.filter(ten_id=mid).exists():
                Tenants.objects.filter(ten_id=mid).delete()
        return CustomResponse(data=res_body, status=200, message="Members deleted successfully.")
    except Exception as e:
        logger.error(f"delete_members error: {e}", exc_info=True)
        return CustomResponse(data=res_body, status=500, message="error")


@api_view(['POST'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
@transaction.atomic
def save_member(request: Request) -> CustomResponse:
    """
    Updates member details, updates plan logs, processes billing/invoices and records TenDLC registration status.
    """
    res_body: Dict[str, Any] = {}
    try:
        member_dto = request.data
        member_id = member_dto.get("memberId")
        tenant = Tenants.objects.select_related('details').filter(ten_id=member_id).first()
        if not tenant:
            return CustomResponse(data=res_body, status=500, message="Error in save member")

        details = getattr(tenant, 'details', None)

        # 1. Plan updates logic
        try:
            profile_id = details.td_authorize_customer_profile_id if details else None
            payment_profile_id = details.td_authorize_customer_payment_profile_id if details else None
            chk_auth = bool(profile_id and payment_profile_id and len(profile_id.strip()) > 0 and len(payment_profile_id.strip()) > 0)
            
            if chk_auth:
                new_plan_id = member_dto.get("planId")
                plan = Plan.objects.filter(planId=new_plan_id).first()

                old_plan_id = int(details.td_plan_id) if details and details.td_plan_id and details.td_plan_id.isdigit() else 1

                if old_plan_id != new_plan_id:
                    old_plan = Plan.objects.filter(planId=old_plan_id).first()
                    if old_plan and (old_plan.planId == 2 or old_plan.planName == "Pay As You Go"):
                        CampaignTransaction.objects.filter(
                            memberId=tenant.ten_id,
                            tranInvoicedStatus="uninvoiced"
                        ).exclude(
                            tranType__in=["sms number", "sms polling number", "sms conversations number"]
                        ).delete()

                    if plan and (plan.planId == 2 or plan.planName == "Pay As You Go"):
                        from accounting_app.views.invoice_views import create_invoice
                        create_invoice(request, tenant.ten_id)

                total_contact_uploaded = Userlist.objects.filter(
                    memberId=tenant.ten_id,
                    badEmail="N",
                    badPhoneNumber="N",
                    status="Subscribed",
                    smsStatus="Subscribed"
                ).filter(Q(optId__isnull=True) | Q(optId=0)).count()

                country_str = tenant.ten_country
                country_id = 100
                if country_str and country_str.strip():
                    try:
                        country_id = int(country_str)
                    except Exception:
                        pass

                try:
                    country_setting = CountrySetting.objects.get(cntyId=country_id, cntyPlanId=new_plan_id)
                except CountrySetting.DoesNotExist:
                    try:
                        country_setting = CountrySetting.objects.get(cntyId=100, cntyPlanId=new_plan_id)
                    except CountrySetting.DoesNotExist:
                        country_setting = CountrySetting.objects.get(cntyId=100, cntyPlanId=2)

                if plan and (total_contact_uploaded <= country_setting.cntyContactsIncluded or plan.planId == 2 or plan.planName == "Pay As You Go"):
                    if details:
                        details.td_plan_id = str(new_plan_id)
                        details.save()

                    try:
                        plan_log = PlanLogs(
                            plogsMemberId=tenant.ten_id,
                            plogsPlanId=new_plan_id,
                            plogsAddedDate=timezone.now()
                        )
                        plan_log.save()
                    except Exception as ee:
                        logger.error(f"Error logging plan change: {ee}")
                else:
                    res_body["error"] = "Your Current Contacts Are Greater Then Selected Plan Contacts.\nPlease Select Other Higher Plan."
            else:
                res_body["error"] = "Please Update Your Payment Profile"
        except Exception as e:
            res_body["error"] = "error"
            logger.error(f"UpdatePlan Error : {e}", exc_info=True)

        # 3. Update the tenant object properties
        tenant.ten_email = DecryptString.setEncDecUser(member_dto.get("email"), "", "Y")
        tenant.ten_first_name = DecryptString.setEncDecUser(member_dto.get("firstName"), "", "Y")
        tenant.ten_last_name = DecryptString.setEncDecUser(member_dto.get("lastName"), "", "Y")
        tenant.ten_country = member_dto.get("country")
        tenant.ten_street_address1 = DecryptString.setEncDecUser(member_dto.get("address"), "", "Y")
        tenant.ten_city = DecryptString.setEncDecUser(member_dto.get("city"), "", "Y")
        tenant.ten_state = DecryptString.setEncDecUser(member_dto.get("state"), "", "Y")
        tenant.ten_post_code = DecryptString.setEncDecUser(member_dto.get("postCode"), "", "Y")
        tenant.ten_phone = DecryptString.setEncDecUser(member_dto.get("phone"), "", "Y")
        tenant.ten_cell_phone = DecryptString.setEncDecUser(member_dto.get("cell"), "", "Y")
        tenant.ten_status = member_dto.get("memberStatus")
        tenant.save()

        # Update TenantDetails properties if available
        if details:
            details.td_password = DecryptString.setEncDecUser(member_dto.get("password"), "", "Y")
            details.td_bill_date = parse_dto_date(member_dto.get("billDate"))
            details.td_is2fa = member_dto.get("is2FA")
            details.td_membership_type = member_dto.get("membershipType")
            details.td_sec_ans_1 = DecryptString.setEncDecUser(member_dto.get("secAns1"), "", "Y")
            details.td_sec_ans_2 = DecryptString.setEncDecUser(member_dto.get("secAns2"), "", "Y")
            details.td_sec_ans_3 = DecryptString.setEncDecUser(member_dto.get("secAns3"), "", "Y")
            details.td_authorize_customer_payment_profile_id = DecryptString.setEncDecUser(member_dto.get("authorizeCustomerPaymentProfileId"), "", "Y")
            details.td_authorize_customer_profile_id = DecryptString.setEncDecUser(member_dto.get("authorizeCustomerProfileId"), "", "Y")
            details.save()

        # 4. MemberStatus logging
        member_status = MemberStatus.objects.filter(memberId=tenant.ten_id).first()
        if member_status:
            member_status.status = member_dto.get("memberStatus")
            member_status.reason = member_dto.get("reason")
            member_status.changeDate = timezone.now().date()
            member_status.save()
        else:
            member_status = MemberStatus(
                memberId=tenant.ten_id,
                status=member_dto.get("memberStatus"),
                reason=member_dto.get("reason"),
                changeDate=timezone.now().date()
            )
            member_status.save()

        # 5. TenDLCData state updates
        ten_dlc_data_dtos = member_dto.get("tenDLCData", [])
        for tdd_dto in ten_dlc_data_dtos:
            dat_id = tdd_dto.get("datId")
            dat_is_active = tdd_dto.get("datIsActive")
            TenDLCData.objects.filter(datId=dat_id).update(datIsActive=dat_is_active)

        return CustomResponse(data=res_body, status=200, message="Member data updated successfully")
    except Exception as ex:
        logger.error(f"save_member error: {ex}", exc_info=True)
        return CustomResponse(data=res_body, status=500, message="Error in save member")


@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_token_by_member_id(request: Request, memberId: int) -> CustomResponse:
    """
    Generates a signed JWT token for a member.
    """
    res_body: Dict[str, Any] = {}
    try:
        tenant = Tenants.objects.filter(ten_id=memberId).first()
        if tenant:
            from auth_app.utils import generate_member_token
            jwt_token = generate_member_token(tenant)
            res_body["memberToken"] = jwt_token
            return CustomResponse(data=res_body, status=200, message="Member fetched successfully")
        else:
            return CustomResponse(data=res_body, status=500, message="Member not found ")
    except Exception as e:
        logger.error(f"get_token_by_member_id error: {e}", exc_info=True)
        return CustomResponse(data=res_body, status=500, message="Member not found ")


@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_download_member_list(request: Request) -> CustomResponse:
    """
    Writes a CSV format file containing all members with decrypted fields to the download folder.
    """
    res_body: Dict[str, Any] = {}
    try:
        csv_download_path = getattr(settings, 'CSVDOWNLOAD_DIR', None)
        if not csv_download_path:
            csv_download_path = settings.BASE_DIR / 'csv_download'
        else:
            csv_download_path = Path(csv_download_path)

        os.makedirs(csv_download_path, exist_ok=True)
        file_path = str(csv_download_path / "member_export_list.csv")

        header = ["Member Id", "User Name", "First Name", "Last Name", "Email", "Cell", "Phone", "Country", "State", "City", "Plan Name", "Member Status", "Login Preference"]
        
        tenants = Tenants.objects.select_related('details').all().order_by('ten_id')

        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(header)

            for tenant in tenants:
                details = getattr(tenant, 'details', None)
                email = DecryptString.setEncDecUser(tenant.ten_email, "display", "Y") or ""
                first_name = DecryptString.setEncDecUser(tenant.ten_first_name, "display", "Y") or ""
                last_name = DecryptString.setEncDecUser(tenant.ten_last_name, "display", "Y") or ""
                cell = DecryptString.setEncDecUser(tenant.ten_cell_phone, "display", "Y") or ""
                phone = DecryptString.setEncDecUser(tenant.ten_phone, "display", "Y") or ""

                country_name = ""
                if tenant.ten_country and tenant.ten_country.strip():
                    try:
                        country_id = int(tenant.ten_country)
                        country_name = Country.objects.filter(id=country_id).values_list('cntName', flat=True).first() or ""
                    except Exception:
                        pass

                state = DecryptString.setEncDecUser(tenant.ten_state, "display", "Y") or ""
                city = DecryptString.setEncDecUser(tenant.ten_city, "display", "Y") or ""

                status_val = ""
                if tenant.ten_status == 0:
                    status_val = "Active"
                elif tenant.ten_status == 1:
                    status_val = "Inactive"
                elif tenant.ten_status == 2:
                    status_val = "Bad Credit Card"
                elif tenant.ten_status == 3:
                    status_val = "Suspended"

                plan_name = ""
                if details and details.td_plan_id:
                    try:
                        plan_id = int(details.td_plan_id)
                        if plan_id > 0:
                            plan = Plan.objects.filter(planId=plan_id).first()
                            if plan:
                                plan_name = plan.planName
                    except ValueError:
                        pass

                username = DecryptString.setEncDecUser(tenant.ten_username, "display", "Y") or ""
                login_pref = details.td_login_preference if details else ""

                row = [
                    str(tenant.ten_id),
                    username,
                    first_name,
                    last_name,
                    email,
                    cell,
                    phone,
                    country_name,
                    state,
                    city,
                    plan_name,
                    status_val,
                    login_pref
                ]
                writer.writerow(row)

        site_url = getattr(settings, 'SITEURL', '')
        if site_url and not site_url.endswith('/'):
            site_url += '/'
        res_body["filePath"] = f"{site_url}csv_download/member_export_list.csv"

        return CustomResponse(data=res_body, status=200, message="Export Member Successfully.")
    except Exception as e:
        logger.error(f"get_download_member_list error: {e}", exc_info=True)
        return CustomResponse(data=res_body, status=500, message="error")