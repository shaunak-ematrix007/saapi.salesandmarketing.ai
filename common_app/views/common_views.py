from typing import Any, Dict, List
import datetime
from django.conf import settings
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from auth_app.authentication import CustomJWTAuthentication
from common_app.models import Language, SecurityQuestion, Country, CountryToState, CountrySetting, Member, Userlist, Udf
from common_app.responses import CustomResponse
from common_app.common_function import CommonFunction, send_email


# Helper Serializers to match Spring Boot Response JSON contract perfectly
def serialize_language(lg: Language) -> Dict[str, Any]:
    return {
        "lgId": lg.lgId,
        "lgDisOrder": lg.lgDisOrder,
        "lgLongName": lg.lgLongName,
        "lgName": lg.lgName
    }


def serialize_security_question(sq: SecurityQuestion) -> Dict[str, Any]:
    return {
        "id": sq.secId,
        "question": sq.secQuestion
    }


def serialize_country(c: Country) -> Dict[str, Any]:
    return {
        "id": c.id,
        "cntCode": c.cntCode,
        "cntName": c.cntName,
        "iso2": c.iso2,
        "longName": c.longName,
        "oid": c.oid,
        "phoneMinLength": c.phoneMinLength,
        "phoneMaxLength": c.phoneMaxLength
    }


def serialize_country_to_state(cts: CountryToState) -> Dict[str, Any]:
    return {
        "countryToStateId": cts.countryToStateId,
        "fkCountryId": cts.fkCountryId,
        "stateCapital": cts.stateCapital,
        "stateLong": cts.stateLong,
        "stateShort": cts.stateShort
    }


def serialize_country_setting(cs: CountrySetting) -> Dict[str, Any]:
    if not cs:
        return {}
    expiry_dt = cs.cntyLinkExpiryDateTime.isoformat() if cs.cntyLinkExpiryDateTime else None
    update_dt = cs.cntyUpdateDateTime.isoformat() if cs.cntyUpdateDateTime else None
    
    return {
        "id": cs.id,
        "cntyId": cs.cntyId,
        "cntyISO2": cs.cntyISO2,
        "cntyName": cs.cntyName,
        "cntyPriceSymbol": cs.cntyPriceSymbol,
        "cntyAssessmentPrice": cs.cntyAssessmentPrice,
        "cntySurveyPrice": cs.cntySurveyPrice,
        "cntyIndividualPrice": cs.cntyIndividualPrice,
        "cntySocialMediaPrice": cs.cntySocialMediaPrice,
        "cntyCampaignPerPrice": cs.cntyCampaignPerPrice,
        "cntySurveyPerPrice": cs.cntySurveyPerPrice,
        "cntyAssessmentPerPrice": cs.cntyAssessmentPerPrice,
        "cntyMMSPerPrice": cs.cntyMMSPerPrice,
        "cntySMSPerPrice": cs.cntySMSPerPrice,
        "cntySMSNumberPerPrice": cs.cntySMSNumberPerPrice,
        "cntyFirstInvFreeAmt": cs.cntyFirstInvFreeAmt,
        "cntyInvLessAmtNotCharge": cs.cntyInvLessAmtNotCharge,
        "cntyTranslateCharCharge": cs.cntyTranslateCharCharge,
        "cntySMSConversationsPerPrice": cs.cntySMSConversationsPerPrice,
        "cntyCallPerMinPrice": cs.cntyCallPerMinPrice,
        "cntyContactsIncluded": cs.cntyContactsIncluded,
        "cntyMaxNumberOfEmail": cs.cntyMaxNumberOfEmail,
        "cntyPlanId": cs.cntyPlanId,
        "cntyPlanPrice": cs.cntyPlanPrice,
        "cntySupport": cs.cntySupport,
        "cntyMultiUser": cs.cntyMultiUser,
        "cntyAutomation": cs.cntyAutomation,
        "cntyWhiteListing": cs.cntyWhiteListing,
        "cntyCalendar": cs.cntyCalendar,
        "cntyZoomConferences": cs.cntyZoomConferences,
        "cntySocialMedia": cs.cntySocialMedia,
        "cntySmsInbox": cs.cntySmsInbox,
        "cntyAbTesting": cs.cntyAbTesting,
        "cntyPlanPopular": cs.cntyPlanPopular,
        "cntyPlanDisplayOrder": cs.cntyPlanDisplayOrder,
        "cntyFormResponse": cs.cntyFormResponse,
        "cntyAdditionalContacts": cs.cntyAdditionalContacts,
        "cntyAdditionalContactsPrice": cs.cntyAdditionalContactsPrice,
        "cnty10DLCPrice": cs.cnty10DLCPrice,
        "cnty10DLCCampaignTypeCharge": cs.cnty10DLCCampaignTypeCharge,
        "cnty10DLCOtherCharge": cs.cnty10DLCOtherCharge,
        "cntyWarmupPrice": cs.cntyWarmupPrice,
        "ctnyAiGeneratedImage": cs.ctnyAiGeneratedImage,
        "ctnyAiEditedImage": cs.ctnyAiEditedImage,
        "ctnyContactPerPrice": cs.ctnyContactPerPrice,
        "cntyLinkExpiryDateTime": expiry_dt,
        "cntyUpdateDateTime": update_dt
    }


# Endpoints Migration: Strictly Function-Based Views

@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def lookup_data(request: Request) -> CustomResponse:
    languages = [serialize_language(lg) for lg in Language.objects.all()]
    security_questions = [serialize_security_question(sq) for sq in SecurityQuestion.objects.all()]
    countries = [serialize_country(c) for c in Country.objects.order_by('oid')]
    states = [serialize_country_to_state(cts) for cts in CountryToState.objects.all()]
    
    res_body = {
        "language": languages,
        "securityQuestion": security_questions,
        "country": countries,
        "state": states
    }
    return CustomResponse(data=res_body, status=200, message="Fetch data successfully.")


@api_view(['POST'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def sending_email(request: Request) -> CustomResponse:
    request_data = request.data
    context = {"Url": getattr(settings, 'SITEURL', '')}
    res = send_email(request_data, context)
    return CustomResponse(
        status=200 if res.get("status") else 500,
        message=res.get("message", "Email failed")
    )


@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def display_language(request: Request) -> CustomResponse:
    languages = Language.objects.all()
    language_dict = {lg.lgName: lg.lgLongName for lg in languages if lg.lgName}
    res_body = {
        "language": language_dict
    }
    return CustomResponse(data=res_body, status=200, message="Fetch language successfully.")


@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def language(request: Request) -> CustomResponse:
    languages = [serialize_language(lg) for lg in Language.objects.all()]
    res_body = {
        "language": languages
    }
    return CustomResponse(data=res_body, status=200, message="Fetch language successfully.")


@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def country(request: Request) -> CustomResponse:
    countries = [serialize_country(c) for c in Country.objects.order_by('oid')]
    res_body = {
        "country": countries
    }
    return CustomResponse(data=res_body, status=200, message="Fetch country successfully.")


@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def country_to_state(request: Request, countryId: int) -> CustomResponse:
    states = [serialize_country_to_state(cts) for cts in CountryToState.objects.filter(fkCountryId=countryId)]
    res_body = {
        "state": states
    }
    return CustomResponse(data=res_body, status=200, message="Fetch state successfully.")


@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def security_question(request: Request) -> CustomResponse:
    security_questions = [serialize_security_question(sq) for sq in SecurityQuestion.objects.all()]
    res_body = {
        "securityQuestion": security_questions
    }
    return CustomResponse(data=res_body, status=200, message="Fetch security question successfully.")


@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_remote_address(request: Request) -> CustomResponse:
    remote_ip = request.META.get('REMOTE_ADDR', '')
    res_body = {
        "remoteAddress": remote_ip
    }
    return CustomResponse(data=res_body, status=200, message="Fetch remote address successfully.")


@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_country_setting(request: Request, countryId: int, planId: int) -> CustomResponse:
    if countryId == 0:
        countryId = 100
    try:
        cs = CountrySetting.objects.get(cntyId=countryId, cntyPlanId=planId)
    except CountrySetting.DoesNotExist:
        try:
            cs = CountrySetting.objects.get(cntyId=100, cntyPlanId=planId)
        except CountrySetting.DoesNotExist:
            cs = None
    
    res_body = {
        "countrySetting": serialize_country_setting(cs)
    }
    return CustomResponse(data=res_body, status=200, message="Fetch country setting successfully.")


@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def country_to_state_name(request: Request, countryName: str) -> CustomResponse:
    try:
        country = Country.objects.get(cntName=countryName)
        country_id = country.id
    except Country.DoesNotExist:
        country_id = 0
    
    if country_id > 0:
        states = [serialize_country_to_state(cts) for cts in CountryToState.objects.filter(fkCountryId=country_id)]
        res_body = {
            "state": states
        }
        return CustomResponse(data=res_body, status=200, message="Fetch state successfully.")
    else:
        return CustomResponse(data={}, status=500, message="Invalid country name.")


@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_country_name(request: Request, countryId: int) -> CustomResponse:
    res_body = {}
    try:
        country = Country.objects.get(id=countryId)
        res_body["countryName"] = country.cntName
    except Country.DoesNotExist:
        res_body["countryName"] = ""
    return CustomResponse(data=res_body, status=200, message="Fetch country successfully.")


@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_country_id(request: Request, countryName: str) -> CustomResponse:
    res_body = {}
    try:
        country = Country.objects.get(cntName=countryName)
        res_body["countryId"] = country.id
    except Country.DoesNotExist:
        res_body["countryId"] = 0
    return CustomResponse(data=res_body, status=200, message="Fetch country successfully.")


# Helper to emulate findGroupFirstRecords raw SQL query and BS4 decryptions
def find_group_first_records_helper(member_id: int, group_id: int) -> Dict[str, Any]:
    from django.db.models import Q
    res_body = {}
    try:
        userlist = list(
            Userlist.objects.filter(
                groupId=group_id,
                memberId=member_id,
                status='Subscribed',
                badEmail='N',
                badPhoneNumber='N',
                optId__in=[None, 0]
            ).filter(
                Q(smsStatus='Subscribed') | Q(smsStatus__isnull=True)
            ).exclude(
                email__isnull=True
            ).exclude(
                email=''
            ).order_by('firstName')[:1]
        )
        if userlist:
            ul = userlist[0]
            email_val = ul.email
            try:
                from common_app.decrypt_string import DecryptString
                decrypted_email = DecryptString.setEncDecUser(email_val, "display", "Y")
            except Exception:
                decrypted_email = email_val
            
            res_body = {
                "First_Name": ul.firstName,
                "Last_Name": ul.lastName,
                "Email": decrypted_email,
                "Contact_No": ul.phoneNumber
            }
            
            udfs = Udf.objects.filter(groupId=group_id)
            for udf in udfs:
                udf_name = udf.udf or ""
                udf_label = udf.udfLabel
                field_name = f"udf{udf_label}"
                udf_val = getattr(ul, field_name, None)
                
                if udf_name == "birthday":
                    try:
                        from common_app.decrypt_string import DecryptString
                        decrypted_udf = DecryptString.setEncDecUser(udf_val, "display", "Y")
                    except Exception:
                        decrypted_udf = udf_val
                    res_body[udf_name.replace(" ", "_")] = decrypted_udf
                else:
                    res_body[udf_name.replace(" ", "_")] = udf_val
    except Exception:
        pass
    
    return res_body


@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_group_first_records(request: Request, groupId: int) -> CustomResponse:
    # Extract user ID using custom auth structure
    if isinstance(request.user, Member):
        member = request.user
    else:
        member_id = getattr(request.user, 'memberId', getattr(request.user, 'memberId', None))
        try:
            member = Member.objects.get(memberId=member_id)
        except Member.DoesNotExist:
            member = None

    if member:
        final_member_id = CommonFunction.getFinalMemberId(member)
        data = find_group_first_records_helper(final_member_id, groupId)
        return CustomResponse(data=data, status=200, message="Fetched first record successfully.")
    
    return CustomResponse(data={}, status=500, message="User session not found.")


@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def check_authorized(request: Request) -> CustomResponse:
    if isinstance(request.user, Member):
        member = request.user
    else:
        member_id = getattr(request.user, 'memberId', getattr(request.user, 'memberId', None))
        try:
            member = Member.objects.get(memberId=member_id)
        except Member.DoesNotExist:
            member = None

    if member:
        final_member_id = CommonFunction.getFinalMemberId(member)
        profile_id = member.authorizeCustomerProfileId
        payment_profile_id = member.authorizeCustomerPaymentProfileId
        
        if profile_id and payment_profile_id and len(profile_id.strip()) > 0 and len(payment_profile_id.strip()) > 0:
            return CustomResponse(status=200, message="Successfully.", data="")

    return CustomResponse(status=500, message="Error processing request.", data="")


@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def validate_phone_format(request: Request, countryId: int, phoneNumber: str) -> CustomResponse:
    try:
        clean_number = CommonFunction.cleanMeNumber(phoneNumber)
        country = Country.objects.get(id=countryId)
        if len(clean_number) == country.phoneMinLength or len(clean_number) == country.phoneMaxLength:
            return CustomResponse(status=200, message="Successfully.", data="")
    except Exception:
        pass
    return CustomResponse(status=500, message="Error processing request.", data="")


@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_price_list(request: Request) -> CustomResponse:
    res_body = {}
    try:
        country_setting = CountrySetting.objects.get(cntyId=100, cntyPlanId=1)
        res_body = {
            "cntyCampaignPerPrice": country_setting.cntyCampaignPerPrice,
            "cntySMSPerPrice": country_setting.cntySMSPerPrice,
            "cntySurveyPerPrice": country_setting.cntySurveyPerPrice,
            "cntyIndividualPrice": country_setting.cntyIndividualPrice
        }
    except CountrySetting.DoesNotExist:
        pass
    return CustomResponse(data=res_body, status=200, message="Fetch price successfully.")
