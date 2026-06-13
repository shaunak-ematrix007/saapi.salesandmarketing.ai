import json
import logging
import math
import urllib.request
import urllib.error
from datetime import datetime
from typing import Any, Dict, List, Tuple

from django.conf import settings
from django.db import transaction, models
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.status import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR

from common_app.models import (
    Member, CountrySetting, CampaignTransaction, Invoice,
    MonthlyCurrentPlan, MonthlyPlanLogs, Plan,
    Settings as GeneralSettings, SpTransLog, SpQuestions, SpOptions,
    SpReply, MemberStatus, Userlist
)
from common_app.responses import CustomResponse
from common_app.decrypt_string import DecryptString
from common_app.common_function import CommonFunction, send_email, MailRequestDTO

logger = logging.getLogger(__name__)

# --- Authorize.Net Helper Logic ---

def is_sandbox() -> bool:
    """Checks whether sandbox environment should be active."""
    envsys = getattr(settings, 'ENVSYS', 'qaapi')
    return envsys != 'prod'

def get_authorizenet_credentials() -> Tuple[str, str]:
    """Retrieves Authorize.Net Login ID and Transaction Key from Django settings."""
    if is_sandbox():
        return (
            getattr(settings, 'AUTHORIZENET_LOGIN_ID', '8F35vjvYt'),
            getattr(settings, 'AUTHORIZENET_TRANSACTION_KEY', '3sewR75M52Ddg85N')
        )
    else:
        return (
            getattr(settings, 'AUTHORIZENET_PRODUCTION_LOGIN_ID', '2ZQ6Tb85nq4R'),
            getattr(settings, 'AUTHORIZENET_PRODUCTION_TRANSACTION_KEY', '5PB8m4gtwEB949gq')
        )

def get_authorizenet_url() -> str:
    """Returns the Authorize.Net endpoint URL based on environment."""
    if is_sandbox():
        return "https://apitest.authorize.net/xml/v1/request.api"
    else:
        return "https://api.authorize.net/xml/v1/request.api"

def call_authorizenet_api(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Performs HTTP request to Authorize.Net JSON API."""
    url = get_authorizenet_url()
    headers = {'Content-Type': 'application/json'}
    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode('utf-8'),
            headers=headers,
            method='POST'
        )
        with urllib.request.urlopen(req, timeout=15) as response:
            res_data = response.read().decode('utf-8')
            if res_data.startswith('\ufeff'):
                res_data = res_data[1:]
            return json.loads(res_data)
    except Exception as e:
        logger.error(f"Error calling Authorize.Net: {e}", exc_info=True)
        return {}

def check_payment_profile_exists(authorize_customer_profile_id: str, authorize_customer_payment_profile_id: str) -> str:
    """Validates if customer profile exists on Authorize.Net."""
    login_id, trans_key = get_authorizenet_credentials()
    payload = {
        "getCustomerProfileRequest": {
            "merchantAuthentication": {
                "name": login_id,
                "transactionKey": trans_key
            },
            "customerProfileId": authorize_customer_profile_id,
            "includeMerchantCustomerId": True
        }
    }
    res = call_authorizenet_api(payload)
    if res and "messages" in res and res["messages"].get("resultCode") == "Ok":
        return "ok"
    return "Invalid customer profile."

def charge_payment_profile(member_id: int, amt: float, inv_no: int) -> Dict[str, Any]:
    """Charges customer payment profile on Authorize.Net."""
    try:
        member = Member.objects.get(memberId=member_id)
        # auth_customer_profile_id = DecryptString.setEncDecUser(member.authorizeCustomerPaymentProfileId, "display", "Y")
        # auth_customer_payment_profile_id = DecryptString.setEncDecUser(member.authorizeCustomerProfileId, "display", "Y")
        
        # Note: Java had swap-like mapping in place:
        # authCustomerProfileId = DecryptString.setEncDecUser(memberDto.getAuthorizeCustomerProfileId(), "display", "Y");
        # authCustomerPaymentProfileId = DecryptString.setEncDecUser(memberDto.getAuthorizeCustomerPaymentProfileId(), "display", "Y");
        # Let's map identically as Java implementation:
        auth_profile = DecryptString.setEncDecUser(member.authorizeCustomerProfileId, "display", "Y")
        auth_payment_profile = DecryptString.setEncDecUser(member.authorizeCustomerPaymentProfileId, "display", "Y")
        
        login_id, trans_key = get_authorizenet_credentials()
        company_name = getattr(settings, 'COMPANY_NAME', 'SAM')
        
        amt_rounded = math.ceil(amt * 1000.0) / 1000.0
        amt_str = f"{amt_rounded:.2f}"
        
        payload = {
            "createTransactionRequest": {
                "merchantAuthentication": {
                    "name": login_id,
                    "transactionKey": trans_key
                },
                "transactionRequest": {
                    "transactionType": "authCaptureTransaction",
                    "amount": amt_str,
                    "profile": {
                        "customerProfileId": auth_profile,
                        "paymentProfile": {
                            "paymentProfileId": auth_payment_profile
                        }
                    },
                    "order": {
                        "invoiceNumber": f"{company_name}-{inv_no}",
                        "description": f"{company_name} Transaction On Date : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                    },
                    "tax": {
                        "amount": "0.00",
                        "name": "WA state sales tax",
                        "description": "Washington state sales tax"
                    },
                    "taxExempt": False
                }
            }
        }
        return call_authorizenet_api(payload)
    except Exception as e:
        logger.error(f"ChargePaymentProfile Error: {e}", exc_info=True)
        return {}

def check_charge_payment_profile(member_id: int, amt: float, inv_no: int) -> Dict[str, str]:
    """Processes capture transaction and handles error mapping."""
    res_body = {
        "invTransationId": "",
        "invPayCardNo": "",
        "errorCode": "",
        "errorMessage": "",
        "resultCode": "error"
    }
    response = charge_payment_profile(member_id, amt, inv_no)
    try:
        if response:
            messages = response.get("messages", {})
            txn_response = response.get("transactionResponse", {})
            if messages.get("resultCode") == "Ok" and txn_response:
                if "messages" in txn_response and txn_response.get("messages"):
                    res_body["invTransationId"] = txn_response.get("transId", "")
                    res_body["invPayCardNo"] = txn_response.get("accountNumber", "")
                    res_body["resultCode"] = "Ok"
                else:
                    errors = txn_response.get("errors", {})
                    if errors and "error" in errors and errors["error"]:
                        error_item = errors["error"][0]
                        res_body["errorCode"] = str(error_item.get("errorCode", ""))
                        res_body["errorMessage"] = error_item.get("errorText", "")
                        res_body["resultCode"] = "error"
            else:
                if txn_response and "errors" in txn_response and txn_response["errors"]:
                    errors = txn_response.get("errors", {})
                    if "error" in errors and errors["error"]:
                        error_item = errors["error"][0]
                        res_body["errorCode"] = str(error_item.get("errorCode", ""))
                        res_body["errorMessage"] = error_item.get("errorText", "")
                elif "message" in messages and messages["message"]:
                    res_body["errorCode"] = str(messages["message"][0].get("code", ""))
                    res_body["errorMessage"] = messages["message"][0].get("text", "")
                res_body["resultCode"] = "error"
        else:
            res_body["resultCode"] = "error"
    except Exception as e:
        logger.error(f"CheckChargePaymentProfile Error: {e}", exc_info=True)
        res_body["resultCode"] = "error"
    return res_body

def delete_payment_profile(member_id: int, authorize_customer_profile_id: str) -> Dict[str, str]:
    """Removes customer profile from Authorize.Net."""
    res_body = {"resultCode": "error"}
    try:
        login_id, trans_key = get_authorizenet_credentials()
        payload = {
            "deleteCustomerProfileRequest": {
                "merchantAuthentication": {
                    "name": login_id,
                    "transactionKey": trans_key
                },
                "customerProfileId": authorize_customer_profile_id
            }
        }
        res = call_authorizenet_api(payload)
        if res and "messages" in res and res["messages"].get("resultCode") == "Ok":
            res_body["resultCode"] = "Ok"
    except Exception as e:
        logger.error(f"DeletePaymentProfile Error: {e}", exc_info=True)
    return res_body

# --- Serialization Helpers ---

def serialize_invoice_dto(invoice: Invoice) -> Dict[str, Any]:
    """Maps Invoice entity to InvoiceDto camelCase properties."""
    ept_inv_id = DecryptString.setEncDecUser(str(invoice.invId), "", "Y")
    ept_member_id = DecryptString.setEncDecUser(str(invoice.memberId), "", "Y")
    
    try:
        inv_status = CampaignTransaction.objects.filter(tranInvoicedId=invoice.invId).values_list('tranInvoicedStatus', flat=True).first()
    except Exception:
        inv_status = None
        
    inv_date_formatted = None
    if invoice.invDate:
        inv_date_formatted = invoice.invDate.strftime("%m/%d/%Y")

    return {
        "invId": invoice.invId,
        "invDate": inv_date_formatted,
        "invNo": invoice.invNo,
        "invTotalAmount": invoice.invTotalAmount,
        "invTransationId": invoice.invTransationId,
        "memberId": invoice.memberId,
        "invClientName": invoice.invClientName,
        "eptInvId": ept_inv_id,
        "eptMemberId": ept_member_id,
        "invStatus": inv_status
    }

def serialize_print_invoice_response_dto(invoice: Invoice) -> Dict[str, Any]:
    """Maps Invoice entity to PrintInvoiceResponseDto properties."""
    inv_date_formatted = None
    if invoice.invDate:
        inv_date_formatted = invoice.invDate.strftime("%Y-%m-%d")
        
    return {
        "invId": invoice.invId,
        "invAdjustmentsAmount": invoice.invAdjustmentsAmount,
        "invAssessmentAmount": invoice.invAssessmentAmount,
        "invAssessmentPrice": invoice.invAssessmentPrice,
        "invBuildItForMeAmount": invoice.invBuildItForMeAmount,
        "invBuildItForMePrice": invoice.invBuildItForMePrice,
        "invCallAmount": invoice.invCallAmount,
        "invCallPrice": invoice.invCallPrice,
        "invCampaignAmount": invoice.invCampaignAmount,
        "invCampaignPrice": invoice.invCampaignPrice,
        "invClientName": invoice.invClientName,
        "invCountryId": invoice.invCountryId,
        "invCurrentContacts": invoice.invCurrentContacts,
        "invDate": inv_date_formatted,
        "invIndividualAmount": invoice.invIndividualAmount,
        "invIndividualPrice": invoice.invIndividualPrice,
        "invMonthlyEmailAmount": invoice.invMonthlyEmailAmount,
        "invMonthlyIndividualAmount": invoice.invMonthlyIndividualAmount,
        "invMonthlySmsAmount": invoice.invMonthlySmsAmount,
        "invMonthlySocialMediaAmount": invoice.invMonthlySocialMediaAmount,
        "invMonthlySurveyAmount": invoice.invMonthlySurveyAmount,
        "invMonthlyYN": invoice.invMonthlyYN,
        "invNo": invoice.invNo,
        "invPageTransAmount": invoice.invPageTransAmount,
        "invPageTransPrice": invoice.invPageTransPrice,
        "invPayCardNo": invoice.invPayCardNo,
        "invSendMail": invoice.invSendMail,
        "invSmsAmount": invoice.invSmsAmount,
        "invSMSConversationsAmount": invoice.invSMSConversationsAmount,
        "invSMSConversationsPrice": invoice.invSMSConversationsPrice,
        "invSmsPollAmount": invoice.invSmsPollAmount,
        "invSmsPollPrice": invoice.invSmsPollPrice,
        "invSmsPrice": invoice.invSmsPrice,
        "invSocialMediaAmount": invoice.invSocialMediaAmount,
        "invSocialMediaPrice": invoice.invSocialMediaPrice,
        "invSubTotal": invoice.invSubTotal,
        "invSurveyAmount": invoice.invSurveyAmount,
        "invSurveyPrice": invoice.invSurveyPrice,
        "invTotalAmount": invoice.invTotalAmount,
        "invTransationId": invoice.invTransationId,
        "subMemberId": invoice.subMemberId,
        "memberId": invoice.memberId,
    }

def get_country_setting(member: Member) -> CountrySetting:
    """Helper method to fetch appropriate CountrySetting parameters."""
    country_id = member.country
    if not country_id or country_id.strip() == "":
        country_id = 100
    else:
        country_id = int(country_id)
        
    plan_id = member.planId
    if plan_id == 0:
        plan_id = 1
        
    try:
        return CountrySetting.objects.get(cntyId=country_id, cntyPlanId=plan_id)
    except CountrySetting.DoesNotExist:
        try:
            return CountrySetting.objects.get(cntyId=100, cntyPlanId=plan_id)
        except CountrySetting.DoesNotExist:
            return CountrySetting.objects.get(cntyId=100, cntyPlanId=2)

def get_serialized_transactions(tran_type: str, member_id: int, inv_id: int) -> List[Dict[str, Any]]:
    if tran_type == "sms":
        cts = CampaignTransaction.objects.filter(memberId=member_id, tranInvoicedId=inv_id, tranType__in=["sms", "sms number"]).order_by('tranId')
    elif tran_type == "sms conversations":
        cts = CampaignTransaction.objects.filter(memberId=member_id, tranInvoicedId=inv_id,
                                                 tranType__in=["sms conversations",
                                                               "sms conversations number"]).order_by('tranId')
    else:
        cts = CampaignTransaction.objects.filter(memberId=member_id, tranInvoicedId=inv_id,
                                                 tranType=tran_type).order_by('tranId')

    result = []
    for ct in cts:
        tran_date_str = None
        if ct.tranCampaignDate:
            try:
                tran_date_str = CommonFunction.displayDate(ct.tranCampaignDate.strftime("%Y-%m-%d"))
            except Exception:
                pass
        inv_date_str = None
        if ct.tranInvoicedDate:
            try:
                inv_date_str = CommonFunction.displayDate(ct.tranInvoicedDate.strftime("%Y-%m-%d"))
            except Exception:
                pass

        result.append({
            "tranId": ct.tranId,
            "tranCampaignId": ct.tranCampaignId,
            "tranCampaignName": CommonFunction.br2nl(ct.tranCampaignName),
            "tranCampaignDate": tran_date_str,
            "tranTotalMember": ct.tranTotalMember,
            "tranType": ct.tranType,
            "tranInvoicedId": ct.tranInvoicedId,
            "tranInvoicedStatus": ct.tranInvoicedStatus,
            "tranInvoicedDate": inv_date_str,
            "memberId": ct.memberId,
            "tranBillType": CommonFunction.getBillType(ct.tranBillType),
            "tranTotalAmount": ct.tranTotalAmount,
            "tranMemberRate": ct.tranMemberRate,
            "tranCountTotalSms": ct.tranCountTotalSms,
            "tranPollFormNo": ct.tranPollFormNo,
            "tranPollToNo": ct.tranPollToNo,
            "subMemberId": ct.subMemberId
        })
    return result

# --- Endpoint Views ---

@api_view(['GET'])
def get_invoice_list_page(request: Request) -> CustomResponse:
    """Returns a paginated list of invoice records, filtered by search criteria."""
    try:
        search_key = request.query_params.get("searchKey", "")
        page = int(request.query_params.get("page", 0))
        size = int(request.query_params.get("size", 10))
        
        offset = page * size
        limit = offset + size
        
        if not search_key:
            invoices = Invoice.objects.all().order_by('-invId')
        else:
            invoices = Invoice.objects.filter(invClientName__icontains=search_key).order_by('-invId')
            
        total_query_count = invoices.count()
        paginated_invoices = invoices[offset:limit]
        
        total_pages = math.ceil(total_query_count / size) if size > 0 else 0
        total_records = Invoice.objects.count()
        
        invoice_dtos = [serialize_invoice_dto(inv) for inv in paginated_invoices]
        
        res_body = {
            "getTotalPages": total_pages,
            "getNumber": page,
            "getSize": size,
            "invoiceListPage": invoice_dtos,
            "getTotalRecords": total_records
        }
        return CustomResponse(data=res_body, status=HTTP_200_OK, message="Invoice Fetched Successfully")
    except Exception as e:
        logger.error(f"getInvoiceListPage error: {e}", exc_info=True)
        return CustomResponse(data={}, status=HTTP_500_INTERNAL_SERVER_ERROR, message="Internal Server Error")

@api_view(['POST'])
def print_invoice(request: Request) -> CustomResponse:
    """Generates the detailed invoice statement including sub-transaction breakdowns."""
    try:
        member_id_enc = request.data.get("memberId")
        inv_id_enc = request.data.get("invId")
        
        if not member_id_enc or not inv_id_enc:
            return CustomResponse(status=HTTP_500_INTERNAL_SERVER_ERROR, message="Invalid Parameters", data="")
            
        member_id = int(DecryptString.setEncDecUser(member_id_enc, "display", "Y"))
        inv_id = int(DecryptString.setEncDecUser(inv_id_enc, "display", "Y"))
        
        monthly_sms_yn = "N"
        monthly_yn = "N"
        
        try:
            inv_obj = Invoice.objects.get(memberId=member_id, invId=inv_id)
        except Invoice.DoesNotExist:
            return CustomResponse(status=HTTP_500_INTERNAL_SERVER_ERROR, message="Invoice not found", data="")
            
        print_invoice_response_dto = serialize_print_invoice_response_dto(inv_obj)
        try:
            print_invoice_response_dto["invDate"] = CommonFunction.displayDate(print_invoice_response_dto["invDate"])
        except Exception:
            pass
        res_body = dict()
        res_body["invoice"] = print_invoice_response_dto
        
        try:
            monthly_inv = Invoice.objects.get(memberId=member_id, invId=inv_id, invMonthlyYN="Y")
            print_invoice_response_monthly_dto = serialize_print_invoice_response_dto(monthly_inv)
            try:
                print_invoice_response_monthly_dto["invDate"] = CommonFunction.displayDate(print_invoice_response_monthly_dto["invDate"])
            except Exception:
                pass
            res_body["invoiceMonthly"] = print_invoice_response_monthly_dto
            
            monthly_yn = print_invoice_response_dto.get("invMonthlyYN", "N")
            if print_invoice_response_dto.get("invMonthlySmsAmount", 0.0) > 0:
                monthly_sms_yn = "Y"
                
            mpl_email = MonthlyPlanLogs.objects.filter(mplMemberId=member_id, mplInvId=inv_id).order_by('-mplPlanEmailQty').values_list('mplPlanEmailQty', flat=True).first() or 0
            mpl_sms = MonthlyPlanLogs.objects.filter(mplMemberId=member_id, mplInvId=inv_id).order_by('-mplPlanSmsQty').values_list('mplPlanSmsQty', flat=True).first() or 0
            mpl_social = MonthlyPlanLogs.objects.filter(mplMemberId=member_id, mplInvId=inv_id).order_by('-mplPlanSocialMediaQty').values_list('mplPlanSocialMediaQty', flat=True).first() or 0
            
            res_body["monthlyPlanLogs"] = {
                "mplPlanEmailQty": mpl_email,
                "mplPlanSmsQty": mpl_sms,
                "mplPlanSocialmediaQty": mpl_social
            }
        except Invoice.DoesNotExist:
            res_body["invoiceMonthly"] = []
            res_body["monthlyPlanLogs"] = []
            


        res_body["campaign"] = get_serialized_transactions("campaign", member_id, inv_id)
        res_body["survey"] = get_serialized_transactions("survey", member_id, inv_id)
        res_body["assessment"] = get_serialized_transactions("assessment", member_id, inv_id)
        res_body["customForm"] = get_serialized_transactions("customform", member_id, inv_id)
        res_body["sms"] = get_serialized_transactions("sms", member_id, inv_id)
        res_body["smsPollingNumber"] = get_serialized_transactions("sms polling number", member_id, inv_id)
        
        sms_polling_list = []
        poll_forms = CampaignTransaction.objects.filter(memberId=member_id, tranInvoicedId=inv_id, tranType="sms polling").values_list('tranPollFormNo', flat=True).distinct()
        for form_no in poll_forms:
            cts = CampaignTransaction.objects.filter(memberId=member_id, tranInvoicedId=inv_id, tranType="sms polling", tranPollFormNo=form_no).order_by('tranId')
            cost = 0.0
            poll_ques = 0
            resp_valid = 0
            resp_invalid = 0
            welcmsg = 0
            camp_name_full = ""
            tran_date = None
            
            for ct in cts:
                camp_name_full = ct.tranCampaignName
                if monthly_yn == "Y" and monthly_sms_yn == "Y":
                    camp_name_full += " - Overage Charges."
                tran_date = ct.tranCampaignDate
                
                sp_logs = SpTransLog.objects.filter(fromNo=ct.tranPollFormNo, toNo=ct.tranPollToNo, smspollingId=ct.tranCampaignId)
                for splog in sp_logs:
                    cost += splog.transAmt
                    msg_contains = splog.msgContains or ""
                    user_reply = splog.userReply or ""
                    question_send = splog.questionSend or ""
                    count_tot_msg = 0.0
                    
                    if splog.quesId != 0:
                        if msg_contains != "":
                            if len(msg_contains) > 160:
                                count_tot_msg = math.ceil(len(msg_contains) / 160.0)
                            else:
                                count_tot_msg = 1.0
                                
                        try:
                            sp_ques = SpQuestions.objects.filter(iSmspollingId=ct.tranCampaignId, queId=splog.quesId).order_by('queId').first()
                            if sp_ques:
                                sp_options = SpOptions.objects.filter(queId=splog.quesId).order_by('optId')
                                valid_flag = 0
                                i = 1
                                for op in sp_options:
                                    option_val = op.optionVal or ""
                                    if sp_ques.queTypeId == 1:
                                        replystr = f"{i}) {option_val}"
                                        replystr2 = f"{i}){option_val}"
                                        user_reply_clean = user_reply.strip().lower()
                                        if (str(i) == user_reply.strip() or 
                                            option_val.strip().lower() == user_reply_clean or 
                                            replystr.strip().lower() == user_reply_clean or 
                                            replystr2.strip().lower() == user_reply_clean):
                                            valid_flag = 1
                                            break
                                    elif sp_ques.queTypeId == 2:
                                        valid_flag = 1
                                    i += 1
                                    
                                if valid_flag == 0:
                                    resp_invalid += 2
                                else:
                                    resp_valid += 1
                        except Exception:
                            pass
                            
                        if question_send == "Y":
                            poll_ques += int(count_tot_msg)
                    elif splog.quesId == 0:
                        if len(msg_contains) > 160:
                            welcmsg += int(math.ceil(len(msg_contains) / 160.0))
                        else:
                            welcmsg += 1
                            
            tran_date_formatted = None
            if tran_date:
                tran_date_formatted = tran_date.strftime("%m/%d/%Y")
                
            sms_polling_list.append({
                "cost": cost,
                "welcmsg": welcmsg,
                "pollQues": poll_ques,
                "respValid": resp_valid,
                "respInvalid": resp_invalid,
                "tranCampaignName": camp_name_full,
                "tranCampaignDate": tran_date_formatted,
                "tranPollFormNo": form_no
            })
            
        res_body["smsPolling"] = sms_polling_list
        res_body["languageTranslation"] = get_serialized_transactions("language translation", member_id, inv_id)
        res_body["socialMediaPosting"] = get_serialized_transactions("social media posting", member_id, inv_id)
        res_body["smsConversations"] = get_serialized_transactions("sms conversations", member_id, inv_id)
        res_body["calling"] = get_serialized_transactions("calling", member_id, inv_id)
        res_body["buildItForMe"] = get_serialized_transactions("builditforme", member_id, inv_id)
        
        return CustomResponse(data=res_body, status=HTTP_200_OK, message="Invoice fetched successfully.")
    except Exception as e:
        logger.error(f"printInvoice error: {e}", exc_info=True)
        return CustomResponse(status=HTTP_500_INTERNAL_SERVER_ERROR, message="Error compiling invoice", data="")

@api_view(['GET'])
@transaction.atomic
def create_invoice(request: Request, member_id: int) -> CustomResponse:
    """Calculates billing amounts, processes payment via Authorize.Net, and records Invoice."""
    res_body = {}
    try:
        try:
            member = Member.objects.get(memberId=member_id)
        except Member.DoesNotExist:
            return CustomResponse(status=HTTP_500_INTERNAL_SERVER_ERROR, message="Invalid Member", data=res_body)
            
        price_monthly = 0.0
        sms_price_monthly = 0.0
        survey_price_monthly = 0.0
        individual_price_monthly = 0.0
        social_media_price_monthly = 0.0
        
        # cp_email_qty = 0
        # cp_sms_qty = 0
        # cp_survey_qty = 0
        # cp_form_qty = 0
        # cp_social_media_qty = 0
        
        monthly_yn = "N"
        # un_inv = 0
        
        # cp_nt_mn_email_active = "N"
        # cp_nt_mn_sms_active = "N"
        # cp_nt_mn_survey_active = "N"
        # cp_nt_mn_form_active = "N"
        # cp_nt_mn_socialmedia_active = "N"
        
        # old_cp_survey_price = 0.0
        # old_cp_form_price = 0.0
        # old_cp_social_media_price = 0.0
        
        # old_cp_survey_qty = 0
        # old_cp_form_qty = 0
        # old_cp_social_media_qty = 0
        
        if member.planMonthlyYn in ["Y", "D"]:
            # findOneActive
            monthly_plan = MonthlyCurrentPlan.objects.filter(
                models.Q(cpEmailActive="Y") | 
                models.Q(cpSmsActive="Y") | 
                models.Q(cpSurveyActive="Y") | 
                models.Q(cpFormActive="Y") | 
                models.Q(cpSocialMediaActive="Y"),
                cpMemberId=member_id
            ).order_by('-cpId').first()
            
            if monthly_plan:
                # cp_nt_mn_email_active = monthly_plan.cpNtMnEmailActive
                # cp_nt_mn_sms_active = monthly_plan.cpNtMnSmsActive
                # cp_nt_mn_survey_active = monthly_plan.cpNtMnSurveyActive
                # cp_nt_mn_form_active = monthly_plan.cpNtMnFormActive
                # cp_nt_mn_socialmedia_active = monthly_plan.cpNtMnSocialMediaActive
                #
                # old_cp_survey_price = monthly_plan.cpSurveyPrice
                # old_cp_form_price = monthly_plan.cpFormPrice
                # old_cp_social_media_price = monthly_plan.cpSocialMediaPrice
                #
                # old_cp_survey_qty = monthly_plan.cpSurveyQty
                # old_cp_form_qty = monthly_plan.cpFormQty
                # old_cp_social_media_qty = monthly_plan.cpSocialMediaQty
                
                monthly_yn = "Y"
                # un_inv = 1
                
                if monthly_plan.cpEmailActive == "Y":
                    price_monthly = monthly_plan.cpEmailPrice
                    # cp_email_qty = monthly_plan.cpEmailQty
                if monthly_plan.cpSmsActive == "Y":
                    sms_price_monthly = monthly_plan.cpSmsPrice
                    # cp_sms_qty = monthly_plan.cpSmsQty
                if monthly_plan.cpSurveyActive == "Y":
                    survey_price_monthly = monthly_plan.cpSurveyPrice
                    # cp_survey_qty = monthly_plan.cpSurveyQty
                if monthly_plan.cpFormActive == "Y":
                    individual_price_monthly = monthly_plan.cpFormPrice
                    # cp_form_qty = monthly_plan.cpFormQty
                    
        # findCronDataMember
        # select * from tbl_member where authorizeCustomerProfileId is not NULL and authorizeCustomerPaymentProfileId is not NULL and Member_Id=:memberId
        cron_members = Member.objects.filter(
            memberId=member_id,
            authorizeCustomerProfileId__isnull=False,
            authorizeCustomerPaymentProfileId__isnull=False
        ).exclude(authorizeCustomerProfileId="").exclude(authorizeCustomerPaymentProfileId="")
        
        for m in cron_members:
            # cc_delete_request = m.ccDeleteRequest
            
            # settingsRepository.findSettingsData()
            # select * from tbl_settings limit 1
            settings_obj = GeneralSettings.objects.first()
            bill_period = 1
            if settings_obj and settings_obj.billPeriod:
                import re
                try:
                    bill_period = int(re.sub(r"[^0-9]", "", settings_obj.billPeriod))
                except Exception:
                    bill_period = 1
                    
            try:
                # update bill date
                today = datetime.now()
                # Java: Date bDate = bYear+"-"+bMonth+"-01 00:00:00";
                b_date_str = f"{today.year}-{today.month:02d}-01 00:00:00"
                b_date = CommonFunction.convertDate(b_date_str)
                # updateBillDate
                next_date = CommonFunction.addMonth(b_date, bill_period)
                m.billDate = next_date.date()
                m.save()
            except Exception as e:
                logger.error(f"createInvoice Error 1: {e}")
                
            country_setting = get_country_setting(member)
            
            first_name = DecryptString.setEncDecUser(member.firstName, "display", "Y")
            last_name = DecryptString.setEncDecUser(member.lastName, "display", "Y")
            inv_client_name = f"{first_name} {last_name}"
            email = DecryptString.setEncDecUser(member.email, "display", "Y")
            
            # max_invoiced_no = 0
            inv_first = "no"
            try:
                # select max(invNo) from tbl_invoice where invCountryId=:countryId
                country_str = member.country or "100"
                max_no = Invoice.objects.filter(invCountryId=int(country_str)).aggregate(models.Max('invNo'))['invNo__max']
                if max_no is not None and max_no > 0:
                    # max_invoiced_no = int(max_no)
                    inv_first = "no"
                else:
                    inv_first = "yes"
            except Exception as e:
                logger.error(f"createInvoice Error 2: {e}")
                
            price = 0.0
            surveyPrice = 0.0
            assessmentPrice = 0.0
            individualPrice = 0.0
            smsPrice = 0.0
            smsPollPrice = 0.0
            pageTransPrice = 0.0
            socialMediaPrice = 0.0
            smsConversationsPrice = 0.0
            shareAppointmentPrice = 0.0
            smsCalendarPrice = 0.0
            additionalContactsPrice = 0.0
            tenDLCPrice = 0.0
            ps = 0.0
            pc = 0.0
            pa = 0.0
            pi = 0.0
            psm = 0.0
            psmPoll = 0.0
            # transflg = 0
            ptr = 0.0
            psom = 0.0
            psc = 0.0
            callingPrice = 0.0
            pcl = 0.0
            sca = 0.0
            sal = 0.0
            acp = 0.0
            
            totalCampaign = 0.0
            totalSurvey = 0.0
            totalAssessment = 0.0
            totalIndividual = 0.0
            totalSms = 0.0
            totalSmsPoll = 0.0
            totalPageTrans = 0.0
            # totalSocialMedia = 0.0
            totalSMSConversations = 0.0
            totalCalling = 0.0
            totalSmsCalendar = 0.0
            totalShareAppointment = 0.0
            totalAdditionalContacts = 0.0
            total10DLC = 0.0
            totalWarmup = 0.0
            warmupPrice = 0.0
            totalEmailVerification = 0.0
            emailVerificationPrice = 0.0
            evp = 0.0
            
            # findUninvoicedList
            # SELECT * FROM tbl_campaign_transaction where Member_Id=:memberId and tranInvoicedStatus='uninvoiced' and tranBillType=0 order by tranId desc
            campaign_transactions = CampaignTransaction.objects.filter(
                memberId=member_id,
                tranInvoicedStatus="uninvoiced",
                tranBillType="0"
            ).order_by('-tranId')
            
            for ct in campaign_transactions:
                # transflg = 1
                if ct.tranType == "campaign":
                    pc = ct.tranMemberRate
                    totalCampaign += ct.tranTotalMember
                    if ct.tranMemberRate > 0:
                        price += (ct.tranTotalMember * ct.tranMemberRate)
                    else:
                        price += CommonFunction.campaignPriceList(ct.tranTotalMember, inv_first, country_setting)
                elif ct.tranType == "survey":
                    ps = ct.tranMemberRate
                    totalSurvey += ct.tranTotalMember
                    if ct.tranMemberRate > 0:
                        surveyPrice += (ct.tranTotalMember * ct.tranMemberRate)
                    else:
                        surveyPrice += CommonFunction.surveyPriceList(ct.tranTotalMember, inv_first, country_setting)
                elif ct.tranType == "assessment":
                    pa = ct.tranMemberRate
                    totalAssessment += ct.tranTotalMember
                    assessmentPrice += (ct.tranTotalMember * ct.tranMemberRate)
                elif ct.tranType == "customform":
                    pi = ct.tranMemberRate
                    totalIndividual += ct.tranTotalMember
                    individualPrice += (ct.tranTotalMember * ct.tranMemberRate)
                elif ct.tranType in ["sms", "sms number"]:
                    totalSms += ct.tranTotalMember
                    smsPrice += ct.tranTotalAmount
                    psm = ct.tranMemberRate
                elif ct.tranType == "sms polling":
                    totalSmsPoll += ct.tranTotalMember
                    smsPollPrice += ct.tranTotalAmount
                    psmPoll = ct.tranMemberRate
                    
                    # spReplyRepository.updateData
                    SpReply.objects.filter(
                        smsPollingId=ct.tranCampaignId,
                        fromNo=ct.tranPollFormNo,
                        toNo=ct.tranPollToNo,
                        tranId=0
                    ).update(tranId=ct.tranId)
                    
                    # spTransLogRepository.updateData
                    SpTransLog.objects.filter(
                        smspollingId=ct.tranCampaignId,
                        fromNo=ct.tranPollFormNo,
                        toNo=ct.tranPollToNo,
                        tranId=0
                    ).update(tranId=ct.tranId)
                elif ct.tranType == "sms polling number":
                    totalSmsPoll += ct.tranTotalMember
                    smsPollPrice += ct.tranTotalAmount
                    psmPoll = ct.tranMemberRate
                elif ct.tranType == "language translation":
                    totalPageTrans += ct.tranTotalMember
                    pageTransPrice += ct.tranTotalAmount
                    ptr = ct.tranMemberRate
                elif ct.tranType in ["sms conversations", "sms conversations number"]:
                    totalSMSConversations += ct.tranTotalMember
                    smsConversationsPrice += ct.tranTotalAmount
                    psc = ct.tranMemberRate
                elif ct.tranType == "calling":
                    totalCalling += ct.tranTotalMember
                    callingPrice += ct.tranTotalAmount
                    pcl = ct.tranMemberRate
                elif ct.tranType == "sms calendar appointment":
                    totalSmsCalendar += ct.tranTotalMember
                    smsCalendarPrice += ct.tranTotalAmount
                    sca = ct.tranMemberRate
                elif ct.tranType == "share appointment link":
                    totalShareAppointment += ct.tranTotalMember
                    shareAppointmentPrice += ct.tranTotalAmount
                    sal = ct.tranMemberRate
                elif ct.tranType == "additional contacts":
                    totalAdditionalContacts += ct.tranTotalMember
                    additionalContactsPrice += ct.tranTotalAmount
                    acp = ct.tranMemberRate
                elif ct.tranType == "10DLC":
                    total10DLC += ct.tranTotalMember
                    tenDLCPrice += ct.tranTotalAmount
                elif ct.tranType == "email warmup":
                    totalWarmup += ct.tranTotalMember
                    warmupPrice += ct.tranTotalAmount
                elif ct.tranType == "email verification":
                    totalEmailVerification += ct.tranTotalMember
                    emailVerificationPrice += ct.tranTotalAmount
                    evp = ct.tranMemberRate
                    
            def format_double(val: float) -> float:
                return float(f"{val:.2f}")
                
            amt = (
                format_double(price) +
                format_double(surveyPrice) +
                format_double(assessmentPrice) +
                format_double(individualPrice) +
                format_double(smsPrice) +
                format_double(smsPollPrice) +
                format_double(pageTransPrice) +
                format_double(socialMediaPrice) +
                format_double(smsConversationsPrice) +
                format_double(callingPrice) +
                format_double(smsCalendarPrice) +
                format_double(shareAppointmentPrice) +
                format_double(additionalContactsPrice) +
                format_double(country_setting.cntyPlanPrice) +
                format_double(tenDLCPrice) +
                format_double(warmupPrice) +
                format_double(emailVerificationPrice)
            )
            
            # flag = 0
            if inv_first == "yes":
                if amt < country_setting.cntyFirstInvFreeAmt:
                    # flag = 1
                    pass
                    
            if monthly_yn == "Y":
                amt += price_monthly + sms_price_monthly + survey_price_monthly + individual_price_monthly + social_media_price_monthly
                # flag = 0
                # transflg = 1
                
            # OVERRIDE matches Java logic exactly:
            amt = 1.0
            flag = 0
            transflg = 1
            
            if flag == 0 and transflg == 1:
                if amt >= country_setting.cntyInvLessAmtNotCharge:
                    inv_pay_card_no = ""
                    # result_code = ""
                    inv_trans_id = ""
                    error_code = ""
                    error_message = ""
                    
                    if member.membershipType == "Free":
                        result_code = "Ok"
                    else:
                        # max_invoiced_no = 0
                        try:
                            country_str = member.country or "100"
                            max_no = Invoice.objects.filter(invCountryId=int(country_str)).aggregate(models.Max('invNo'))['invNo__max']
                            if max_no is not None:
                                max_invoiced_no = int(max_no) + 1
                            else:
                                max_invoiced_no = 1
                        except Exception:
                            max_invoiced_no = 1
                            
                        res_inner = check_charge_payment_profile(member_id, amt, max_invoiced_no)
                        result_code = res_inner.get("resultCode")
                        error_code = res_inner.get("errorCode")
                        error_message = res_inner.get("errorMessage")
                        inv_pay_card_no = res_inner.get("invPayCardNo")
                        inv_trans_id = res_inner.get("invTransationId")
                        
                    if result_code == "Ok":
                        # max_invoiced_no = 0
                        try:
                            country_str = member.country or "100"
                            max_no = Invoice.objects.filter(invCountryId=int(country_str)).aggregate(models.Max('invNo'))['invNo__max']
                            if max_no is not None:
                                max_invoiced_no = int(max_no) + 1
                            else:
                                max_invoiced_no = 1
                        except Exception:
                            max_invoiced_no = 1
                            
                        # findByPlanId
                        plan_obj = Plan.objects.filter(planId=member.planId).first()
                        
                        # totalContactUploaded
                        cur_contacts = Userlist.objects.filter(memberId=member_id, badEmail='N', badPhoneNumber='N', status='Subscribed', smsStatus='Subscribed').filter(models.Q(optId__isnull=True) | models.Q(optId=0)).count()
                        
                        invoice = Invoice(
                            invNo=max_invoiced_no,
                            invDate=timezone.now().date(),
                            invCampaignAmount=price,
                            invSurveyAmount=surveyPrice,
                            invAssessmentAmount=assessmentPrice,
                            invIndividualAmount=individualPrice,
                            invSmsAmount=smsPrice,
                            invSmsPollAmount=smsPollPrice,
                            invPageTransAmount=pageTransPrice,
                            invSocialMediaAmount=socialMediaPrice,
                            invSMSConversationsAmount=smsConversationsPrice,
                            invCallAmount=callingPrice,
                            invShareAppointmentAmount=shareAppointmentPrice,
                            invSmsCalendarAmount=smsCalendarPrice,
                            inv10DLCAmount=tenDLCPrice,
                            invWarmupAmount=warmupPrice,
                            invEmailVerificationAmount=emailVerificationPrice,
                            invAdditionalContactsAmount=additionalContactsPrice,
                            invTotalAmount=amt,
                            memberId=member_id,
                            invClientName=inv_client_name,
                            invCampaignPrice=pc,
                            invSurveyPrice=ps,
                            invAssessmentPrice=pa,
                            invIndividualPrice=pi,
                            invSmsPrice=psm,
                            invSmsPollPrice=psmPoll,
                            invPageTransPrice=ptr,
                            invSocialMediaPrice=psom,
                            invSMSConversationsPrice=psc,
                            invCallPrice=pcl,
                            invShareAppointmentPrice=sal,
                            invSmsCalendarPrice=sca,
                            invAdditionalContactsPrice=acp,
                            invCountryId=country_setting.cntyId,
                            invSubTotal=amt,
                            invCurrentContacts=cur_contacts,
                            invEmailVerificationPrice=evp,
                            invPayCardNo=inv_pay_card_no,
                            invMonthlyYN="N",
                            invTransationId=inv_trans_id
                        )
                        if member.membershipType == "Free":
                            invoice.invAdjustmentsAmount = amt
                            
                        if plan_obj:
                            invoice.invPlanId = plan_obj.planId
                            invoice.invPlanPrice = country_setting.cntyPlanPrice
                            invoice.invPlanName = plan_obj.planName
                            
                        invoice.save()
                        inv_id = invoice.invId
                        
                        tran_invoiced_status = "Adjustment - Free Account" if member.membershipType == "Free" else "invoiced"
                        CampaignTransaction.objects.filter(
                            memberId=member_id,
                            tranInvoicedStatus="uninvoiced",
                            tranBillType="0"
                        ).update(
                            tranInvoicedId=inv_id,
                            tranInvoicedStatus=tran_invoiced_status,
                            tranInvoicedDate=timezone.now().date()
                        )
                        
                        site_name = getattr(settings, 'SITENAME', 'SAM')
                        price_symbol = country_setting.cntyPriceSymbol or '$'
                        msg = f"Thank you for your payment.<br><br>{site_name} has charged your card for {price_symbol}{amt:.2f}."
                        res_body["msg"] = msg
                        return CustomResponse(data=res_body, status=HTTP_200_OK, message="Invoice Created successfully")
                    else:
                        # str_err = ""
                        if error_code == "7":
                            str_err = " Credit card expiration date is invalid"
                        elif error_code in ["6", "37"]:
                            str_err = " The credit card number is invalid"
                        elif error_code == "165":
                            str_err = " Please confirm your CVV is correct"
                        elif error_code == "8":
                            str_err = " Credit card has expired"
                            try:
                                mem = Member.objects.get(memberId=member_id)
                                mem.memberStatus = 2
                                mem.save()
                            except Exception:
                                pass
                                
                            try:
                                member_status = MemberStatus.objects.filter(memberId=member_id).first()
                                if not member_status:
                                    member_status = MemberStatus(memberId=member_id)
                                member_status.status = 2
                                member_status.save()
                            except Exception:
                                pass
                                
                            # Send bad credit card email
                            try:
                                mail_dto: MailRequestDTO = {
                                    "to": email,
                                    "templateName": "bad-credit-card-template",
                                    "subject": f"{getattr(settings, 'SITENAME', 'SAM')} Bad Credit Card",
                                    "fromAdd": None,
                                    "replyToAdd": None,
                                    "name": None,
                                    "fileName": None,
                                    "filePath": None
                                }
                                mail_context = {
                                    "invClientName": inv_client_name,
                                    "error": error_message,
                                    "cardNumber": inv_pay_card_no,
                                    "SITEURL": getattr(settings, 'SITEURL', ''),
                                    "supportSiteUrl": getattr(settings, 'SITEURL', ''),
                                    "siteUrlWWW": getattr(settings, 'SITEURLWWW', ''),
                                    "siteUrlWWWDisplay": getattr(settings, 'SITEURLWWWDISPLAY', ''),
                                    "companyName": getattr(settings, 'COMPANY_NAME', 'SAM'),
                                    "mainCompanyName": getattr(settings, 'MAIN_COMPANY_NAME', ''),
                                    "siteUrlAddress": getattr(settings, 'SITEURLADDRESS', ''),
                                    "siteUrlAddressBr": getattr(settings, 'SITEURLADDRESSBR', ''),
                                    "companyNumber": getattr(settings, 'COMPANY_NUMBER', ''),
                                    "siteNameSmallCom": getattr(settings, 'SITENAME_SMALL_COM', ''),
                                    "siteNameBigCom": getattr(settings, 'SITENAME_BIG_COM', '')
                                }
                                send_email(mail_dto, mail_context)
                            except Exception as em:
                                logger.error(f"Error sending bad credit card email: {em}")
                        else:
                            str_err = f" {error_message}"
                            
                        res_body["msg"] = str_err
                        return CustomResponse(status=HTTP_500_INTERNAL_SERVER_ERROR, message=str_err, data=res_body)
                        
        return CustomResponse(data=res_body, status=HTTP_200_OK, message="Invoice Created successfully")
    except Exception as e:
        logger.error(f"createInvoice error: {e}", exc_info=True)
        return CustomResponse(status=HTTP_500_INTERNAL_SERVER_ERROR, message="Error creating invoice", data=res_body)
