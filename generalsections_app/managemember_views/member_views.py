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
    Member, Userlist, Plan, CountrySetting, Country,
    MemberStatus, TenDLCLogs, TenDLCRenew, TenDLCData,
    PlanLogs, CampaignTransaction
)
from common_app.responses import CustomResponse
from common_app.common_function import CommonFunction, send_email, MailRequestDTO
from common_app.decrypt_string import DecryptString

logger = logging.getLogger(__name__)


def serialize_member_dto(member: Member) -> Dict[str, Any]:
    """Helper to serialize Member properties for list views matching MemberDto.java contract."""
    email = DecryptString.setEncDecUser(member.email, "display", "Y") or ""
    first_name = DecryptString.setEncDecUser(member.firstName, "display", "Y") or ""
    last_name = DecryptString.setEncDecUser(member.lastName, "display", "Y") or ""
    cell = DecryptString.setEncDecUser(member.cell, "display", "Y") or ""
    
    member_type = "SubUser" if member.parentMemberId and member.parentMemberId > 0 else "User"
    
    status_val = ""
    if member.memberStatus == 0:
        status_val = "Active"
    elif member.memberStatus == 1:
        status_val = "Inactive"
    elif member.memberStatus == 2:
        status_val = "Bad Credit Card"
    elif member.memberStatus == 3:
        status_val = "Suspended"
        
    plan_name = ""
    if member.planId > 0:
        plan = Plan.objects.filter(planId=member.planId).first()
        if plan:
            plan_name = plan.planName
            
    username = DecryptString.setEncDecUser(member.username, "display", "Y") or ""
    
    return {
        "memberId": member.memberId,
        "email": email,
        "firstName": first_name,
        "lastName": last_name,
        "cell": cell,
        "memberType": member_type,
        "memberStatusValue": status_val,
        "billDate": str(member.billDate) if member.billDate else None,
        "lastLoggedin": str(member.lastLoggedin) if member.lastLoggedin else None,
        "planName": plan_name,
        "username": username,
        "loginPreference": member.loginPreference
    }


def serialize_member_full(member: Member) -> Dict[str, Any]:
    """Helper to serialize Member properties for detailed views matching MemberDto.java contract."""
    return {
        "memberId": member.memberId,
        "membershipType": member.membershipType,
        "password": DecryptString.setEncDecUser(member.password, "display", "Y") or "",
        "companyName": DecryptString.setEncDecUser(member.companyName, "display", "Y") or "",
        "firstName": DecryptString.setEncDecUser(member.firstName, "display", "Y") or "",
        "lastName": DecryptString.setEncDecUser(member.lastName, "display", "Y") or "",
        "memberFullName": f"{DecryptString.setEncDecUser(member.firstName, 'display', 'Y') or ''} {DecryptString.setEncDecUser(member.lastName, 'display', 'Y') or ''}".strip(),
        "address": DecryptString.setEncDecUser(member.address, "display", "Y") or "",
        "streetAddress": DecryptString.setEncDecUser(member.streetAddress, "display", "Y") or "",
        "city": DecryptString.setEncDecUser(member.city, "display", "Y") or "",
        "state": DecryptString.setEncDecUser(member.state, "display", "Y") or "",
        "postCode": DecryptString.setEncDecUser(member.postCode, "display", "Y") or "",
        "country": member.country if member.country is not None else "",
        "phone": DecryptString.setEncDecUser(member.phone, "display", "Y") or "",
        "fax": member.fax,
        "cell": DecryptString.setEncDecUser(member.cell, "display", "Y") or "",
        "email": DecryptString.setEncDecUser(member.email, "display", "Y") or "",
        "memberStatus": member.memberStatus,
        "businessName": DecryptString.setEncDecUser(member.businessName, "display", "Y") or "",
        "websiteName": member.websiteName,
        "newsletterSubscribe": member.newsletterSubscribe,
        "is2FA": member.is2FA,
        "twilioNumberPurchaseDt": str(member.twilioNumberPurchaseDt) if member.twilioNumberPurchaseDt else None,
        "twilioNumberRenewDt": str(member.twilioNumberRenewDt) if member.twilioNumberRenewDt else None,
        "dateRegistered": str(member.dateRegistered) if member.dateRegistered else None,
        "lastLoggedin": str(member.lastLoggedin) if member.lastLoggedin else None,
        "campEmailServers": member.campEmailServers,
        "publicWebAdd": member.publicWebAdd,
        "pusername": member.pusername,
        "ppassword": member.ppassword,
        "paypalTransactionid": member.paypalTransactionid,
        "usedPlanId": member.usedPlanId,
        "authorizeCustomerPaymentProfileId": DecryptString.setEncDecUser(member.authorizeCustomerPaymentProfileId, "display", "Y") or "",
        "authorizeCustomerProfileId": DecryptString.setEncDecUser(member.authorizeCustomerProfileId, "display", "Y") or "",
        "betacode": member.betacode,
        "betalimit": member.betalimit,
        "billDate": str(member.billDate) if member.billDate else None,
        "billDay": member.billDay,
        "ccDeleteRequest": member.ccDeleteRequest,
        "memberDefaultLanguage": member.memberDefaultLanguage,
        "optin": member.optin,
        "parentMemberId": member.parentMemberId,
        "performance": member.performance,
        "planMonthlyYn": member.planMonthlyYn,
        "promotionEAS": member.promotionEAS,
        "secAns1": DecryptString.setEncDecUser(member.secAns1, "display", "Y") or "",
        "secAns2": DecryptString.setEncDecUser(member.secAns2, "display", "Y") or "",
        "secAns3": DecryptString.setEncDecUser(member.secAns3, "display", "Y") or "",
        "secQus1": member.secQus1,
        "secQus2": member.secQus2,
        "secQus3": member.secQus3,
        "shopifyStoreName": member.shopifyStoreName,
        "shopifyStoreToken": member.shopifyStoreToken,
        "smFbAccessToken": member.smFbAccessToken,
        "smFbId": member.smFbId,
        "smLinAuthToken": member.smLinAuthToken,
        "smLinExpiresAt": member.smLinExpiresAt,
        "smTwOauthToken": member.smTwOauthToken,
        "smTwOauthTokenSecret": member.smTwOauthTokenSecret,
        "smsConversationYn": member.smsConversationYn,
        "smsCvrMyphoneYn": member.smsCvrMyphoneYn,
        "subaccountTypeId": member.subaccountTypeId,
        "subAccountAuthToken": member.subAccountAuthToken,
        "subAccountPhoneSId": member.subAccountPhoneSId,
        "subAccountSId": member.subAccountSId,
        "subFriendlyName": member.subFriendlyName,
        "totalEmailLimit": member.totalEmailLimit,
        "totalSubscribeLimit": member.totalSubscribeLimit,
        "totalSurveysLimit": member.totalSurveysLimit,
        "twilioNumber": member.twilioNumber,
        "imageUrl": member.imageUrl,
        "otp": member.otp,
        "twoFANo": member.twoFANo if member.twoFANo is not None else "",
        "smsAllowFlg": member.smsAllowFlg,
        "smsWhiteFlag": member.smsWhiteFlag,
        "planId": member.planId,
        "authKey": member.authKey,
        "authToken": member.authToken,
        "conversationsSubAccountPhoneSId": member.conversationsSubAccountPhoneSId,
        "conversationsTwilioNumberPurchaseDt": str(member.conversationsTwilioNumberPurchaseDt) if member.conversationsTwilioNumberPurchaseDt else None,
        "conversationsTwilioNumber": member.conversationsTwilioNumber,
        "conversationsTwilioNumberRenewDt": str(member.conversationsTwilioNumberRenewDt) if member.conversationsTwilioNumberRenewDt else None,
        "defaultConversationsSubAccountPhoneSId": member.defaultConversationsSubAccountPhoneSId,
        "defaultConversationsTwilioNumber": member.defaultConversationsTwilioNumber,
        "emailNotification": member.emailNotification,
        "enableApi": member.enableApi,
        "googleCalendarAccessToken": member.googleCalendarAccessToken,
        "googleCalendarEmail": member.googleCalendarEmail,
        "googleCalendarRefreshToken": member.googleCalendarRefreshToken,
        "googleCalendarSyncTime": member.googleCalendarSyncTime,
        "linkSendDt": str(member.linkSendDt) if member.linkSendDt else None,
        "outlookCalendarAccessToken": member.outlookCalendarAccessToken,
        "outlookCalendarEmail": member.outlookCalendarEmail,
        "outlookCalendarRefreshToken": member.outlookCalendarRefreshToken,
        "outlookCalendarSyncTime": member.outlookCalendarSyncTime,
        "timeZone": member.timeZone,
        "updatePromotion": member.updatePromotion,
        "updateSupport": member.updateSupport,
        "usedEmailLimit": member.usedEmailLimit,
        "usedSubscribeLimit": member.usedSubscribeLimit,
        "usedSurveysLimit": member.usedSurveysLimit,
        "webConference": member.webConference,
        "zoomToken": member.zoomToken,
        "username": DecryptString.setEncDecUser(member.username, "display", "Y") or "",
        "loginPreference": member.loginPreference
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
    Translates logic from MemberServiceImpl.getMemberListPages.
    """
    res_body: Dict[str, Any] = {}
    try:
        search_key = request.query_params.get("searchKey", "")
        page = int(request.query_params.get("page", 0))
        size = int(request.query_params.get("size", 10))

        offset = page * size
        limit = offset + size

        queryset = Member.objects.all().order_by('memberId')

        if search_key:
            # Match the Java behavior of encrypting the search term before querying
            search_key_enc = DecryptString.setEncDecUser(search_key, "", "Y")
            queryset = queryset.filter(
                Q(firstName__icontains=search_key_enc) |
                Q(lastName__icontains=search_key_enc) |
                Q(email__icontains=search_key_enc)
            )

        total_records = Member.objects.count()
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
    Translates logic from MemberServiceImpl.getMemberById.
    """
    res_body: Dict[str, Any] = {}
    try:
        member = Member.objects.filter(memberId=memberId).first()
        if member:
            res_body["member"] = serialize_member_full(member)
            
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
    Translates logic from MemberServiceImpl.deleteMembers.
    """
    res_body: Dict[str, Any] = {}
    try:
        member_ids = request.data.get("memberIds", [])
        for mid in member_ids:
            if Member.objects.filter(memberId=mid).exists():
                Member.objects.filter(memberId=mid).delete()
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
    Translates logic from MemberServiceImpl.saveMember.
    """
    res_body: Dict[str, Any] = {}
    try:
        member_dto = request.data
        member_id = member_dto.get("memberId")
        member = Member.objects.filter(memberId=member_id).first()
        if not member:
            return CustomResponse(data=res_body, status=500, message="Error in save member")

        # 1. Plan updates logic
        try:
            profile_id = member.authorizeCustomerProfileId
            payment_profile_id = member.authorizeCustomerPaymentProfileId
            chk_auth = bool(profile_id and payment_profile_id and len(profile_id.strip()) > 0 and len(payment_profile_id.strip()) > 0)
            
            if chk_auth:
                new_plan_id = member_dto.get("planId")
                plan = Plan.objects.filter(planId=new_plan_id).first()

                old_plan_id = member.planId if member.planId > 0 else 1

                if old_plan_id != new_plan_id:
                    old_plan = Plan.objects.filter(planId=old_plan_id).first()
                    if old_plan and (old_plan.planId == 2 or old_plan.planName == "Pay As You Go"):
                        # deleteOldUninvoiced
                        CampaignTransaction.objects.filter(
                            memberId=member.memberId,
                            tranInvoicedStatus="uninvoiced"
                        ).exclude(
                            tranType__in=["sms number", "sms polling number", "sms conversations number"]
                        ).delete()

                    if plan and (plan.planId == 2 or plan.planName == "Pay As You Go"):
                        # generateInvoiced
                        from accounting_app.views.invoice_views import create_invoice
                        create_invoice(request, member.memberId)

                # Count contacts to check limits
                total_contact_uploaded = Userlist.objects.filter(
                    memberId=member.memberId,
                    badEmail="N",
                    badPhoneNumber="N",
                    status="Subscribed",
                    smsStatus="Subscribed"
                ).filter(Q(optId__isnull=True) | Q(optId=0)).count()

                country_str = member.country
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
                    member.planId = new_plan_id
                    member.save()

                    try:
                        plan_log = PlanLogs(
                            plogsMemberId=member.memberId,
                            plogsPlanId=member.planId,
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

        # 2. TenDLC status change logic
        if member.tenDLCStatus != member_dto.get("tenDLCStatus"):
            country_str = member.country
            country_id = 100
            if country_str and country_str.strip():
                try:
                    country_id = int(country_str)
                except Exception:
                    pass

            try:
                country_setting = CountrySetting.objects.get(cntyId=country_id, cntyPlanId=member.planId)
            except CountrySetting.DoesNotExist:
                try:
                    country_setting = CountrySetting.objects.get(cntyId=100, cntyPlanId=member.planId)
                except CountrySetting.DoesNotExist:
                    country_setting = CountrySetting.objects.get(cntyId=100, cntyPlanId=2)

            ten_dlc_logs = TenDLCLogs(
                memberId=member.memberId,
                dlcStatus=member_dto.get("tenDLCStatus"),
                dlcDate=timezone.now()
            )
            ten_dlc_logs.save()

            if member_dto.get("tenDLCStatus") == "No":
                ten_dlc_renew = TenDLCRenew(
                    rnwMemberId=member.memberId,
                    rnwContinue="No",
                    rnwDate=timezone.now().date()
                )
                ten_dlc_renew.save()

            if member_dto.get("tenDLCStatus") == "Approved":
                camp_tran1 = CampaignTransaction(
                    tranCampaignName="10DLC Process Charges",
                    tranCampaignDate=timezone.now(),
                    tranTotalMember=1,
                    tranType="10DLC",
                    memberId=member.memberId,
                    tranBillType="0",
                    tranTotalAmount=country_setting.cnty10DLCPrice,
                    tranMemberRate=country_setting.cnty10DLCPrice,
                    tranCountTotalSms=0,
                    tranInvoicedStatus="uninvoiced"
                )
                camp_tran1.save()

                camp_tran2 = CampaignTransaction(
                    tranCampaignName="10DLC Campaign Type Charges",
                    tranCampaignDate=timezone.now(),
                    tranTotalMember=1,
                    tranType="10DLC",
                    memberId=member.memberId,
                    tranBillType="0",
                    tranTotalAmount=country_setting.cnty10DLCCampaignTypeCharge,
                    tranMemberRate=country_setting.cnty10DLCCampaignTypeCharge,
                    tranCountTotalSms=0,
                    tranInvoicedStatus="uninvoiced"
                )
                camp_tran2.save()

                ten_dlc_renew = TenDLCRenew(
                    rnwMemberId=member.memberId,
                    rnwContinue="Yes",
                    rnwDate=timezone.now().date()
                )
                ten_dlc_renew.save()

                # Send template email approval
                try:
                    email_dec = DecryptString.setEncDecUser(member.email, "display", "Y")
                    if email_dec:
                        email_dec = email_dec.lower().strip()
                    
                    first_dec = DecryptString.setEncDecUser(member.firstName, "display", "Y") or ""
                    last_dec = DecryptString.setEncDecUser(member.lastName, "display", "Y") or ""
                    
                    msg_body = f"<p>Hello "
                    if first_dec:
                        msg_body += CommonFunction.ucFirst(first_dec)
                    if last_dec:
                        msg_body += " " + CommonFunction.ucFirst(last_dec)
                    msg_body += "</p>"
                    msg_body += "<p>Your 10DLC Registration Successfully.</p>"

                    mail_dto:MailRequestDTO = {
                        "to": email_dec,
                        "templateName": "approval-10dlc-template",
                        "subject": "10DLC Request Approved",
                        "fromAdd": None,
                        "replyToAdd": None,
                        "name": None,
                        "fileName": None,
                        "filePath": None
                    }

                    mail_context = {
                        "SITEURL": getattr(settings, 'SITEURL', ''),
                        "siteUrlWWW": getattr(settings, 'SITEURLWWW', ''),
                        "siteName": getattr(settings, 'SITENAME', 'SAM'),
                        "supportEmail": getattr(settings, 'SUPPORT_EMAIL', ''),
                        "siteUrlWWWDisplay": getattr(settings, 'SITEURLWWWDISPLAY', ''),
                        "companyName": getattr(settings, 'COMPANY_NAME', 'SAM'),
                        "mainCompanyName": getattr(settings, 'MAIN_COMPANY_NAME', ''),
                        "siteUrlAddress": getattr(settings, 'SITEURLADDRESS', ''),
                        "siteUrlAddressBr": getattr(settings, 'SITEURLADDRESSBR', ''),
                        "companyNumber": getattr(settings, 'COMPANY_NUMBER', ''),
                        "siteNameSmallCom": getattr(settings, 'SITENAME_SMALL_COM', ''),
                        "siteNameBigCom": getattr(settings, 'SITENAME_BIG_COM', ''),
                        "msgBody": CommonFunction.stripSlashes(msg_body)
                    }
                    send_email(mail_dto, mail_context)
                except Exception as ee:
                    logger.error(f"Set10DLCStatus email error: {ee}")
                
                member_dto["smsAllowFlg"] = 1
                member_dto["smsWhiteFlag"] = 1

        # 3. Update the member object properties
        member.tenDLCStatus = member_dto.get("tenDLCStatus")
        member.companyName = DecryptString.setEncDecUser(member_dto.get("companyName"), "", "Y")
        member.email = DecryptString.setEncDecUser(member_dto.get("email"), "", "Y")
        member.password = DecryptString.setEncDecUser(member_dto.get("password"), "", "Y")
        member.firstName = DecryptString.setEncDecUser(member_dto.get("firstName"), "", "Y")
        member.lastName = DecryptString.setEncDecUser(member_dto.get("lastName"), "", "Y")
        member.country = member_dto.get("country")
        member.address = DecryptString.setEncDecUser(member_dto.get("address"), "", "Y")
        member.city = DecryptString.setEncDecUser(member_dto.get("city"), "", "Y")
        member.state = DecryptString.setEncDecUser(member_dto.get("state"), "", "Y")
        member.postCode = DecryptString.setEncDecUser(member_dto.get("postCode"), "", "Y")
        member.phone = DecryptString.setEncDecUser(member_dto.get("phone"), "", "Y")
        member.cell = DecryptString.setEncDecUser(member_dto.get("cell"), "", "Y")
        member.billDate = parse_dto_date(member_dto.get("billDate"))
        member.is2FA = member_dto.get("is2FA")
        member.membershipType = member_dto.get("membershipType")
        member.twoFANo = member_dto.get("twoFANo")
        member.smsAllowFlg = member_dto.get("smsAllowFlg")
        member.smsWhiteFlag = member_dto.get("smsWhiteFlag")
        member.memberStatus = member_dto.get("memberStatus")
        member.secAns1 = DecryptString.setEncDecUser(member_dto.get("secAns1"), "", "Y")
        member.secAns2 = DecryptString.setEncDecUser(member_dto.get("secAns2"), "", "Y")
        member.secAns3 = DecryptString.setEncDecUser(member_dto.get("secAns3"), "", "Y")
        member.businessName = DecryptString.setEncDecUser(member_dto.get("businessName"), "", "Y")
        member.authorizeCustomerPaymentProfileId = DecryptString.setEncDecUser(member_dto.get("authorizeCustomerPaymentProfileId"), "", "Y")
        member.authorizeCustomerProfileId = DecryptString.setEncDecUser(member_dto.get("authorizeCustomerProfileId"), "", "Y")
        member.save()

        # 4. MemberStatus logging
        member_status = MemberStatus.objects.filter(memberId=member.memberId).first()
        if member_status:
            member_status.status = member_dto.get("memberStatus")
            member_status.reason = member_dto.get("reason")
            member_status.changeDate = timezone.now().date()
            member_status.save()
        else:
            member_status = MemberStatus(
                memberId=member.memberId,
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
    Translates logic from MemberServiceImpl.getTokenByMemberId.
    """
    res_body: Dict[str, Any] = {}
    try:
        member = Member.objects.filter(memberId=memberId).first()
        if member:
            from auth_app.utils import generate_member_token
            # Note: We pass the member model to generate the token (with encrypted fields matching Java DTO mapping)
            jwt_token = generate_member_token(member)
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
    Writes a CSV format file containing all members with decrypted fields to the download folder,
    returning the access path URL.
    Translates logic from MemberServiceImpl.getDownloadMemberList.
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
        
        members = Member.objects.all().order_by('memberId')

        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(header)

            for member in members:
                email = DecryptString.setEncDecUser(member.email, "display", "Y") or ""
                first_name = DecryptString.setEncDecUser(member.firstName, "display", "Y") or ""
                last_name = DecryptString.setEncDecUser(member.lastName, "display", "Y") or ""
                cell = DecryptString.setEncDecUser(member.cell, "display", "Y") or ""
                phone = DecryptString.setEncDecUser(member.phone, "display", "Y") or ""

                country_name = ""
                if member.country and member.country.strip():
                    try:
                        country_id = int(member.country)
                        country_name = Country.objects.filter(id=country_id).values_list('cntName', flat=True).first() or ""
                    except Exception:
                        pass

                state = DecryptString.setEncDecUser(member.state, "display", "Y") or ""
                city = DecryptString.setEncDecUser(member.city, "display", "Y") or ""

                status_val = ""
                if member.memberStatus == 0:
                    status_val = "Active"
                elif member.memberStatus == 1:
                    status_val = "Inactive"
                elif member.memberStatus == 2:
                    status_val = "Bad Credit Card"
                elif member.memberStatus == 3:
                    status_val = "Suspended"

                plan_name = ""
                if member.planId > 0:
                    plan = Plan.objects.filter(planId=member.planId).first()
                    if plan:
                        plan_name = plan.planName

                username = DecryptString.setEncDecUser(member.username, "display", "Y") or ""
                login_pref = member.loginPreference or ""

                row = [
                    str(member.memberId),
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
