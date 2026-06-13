import logging
import math
from typing import Any, Dict, Optional
from django.db import transaction
from django.db.models import Max
from django.utils import timezone
from django.conf import settings

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated

from auth_app.authentication import CustomJWTAuthentication
from common_app.models import CountrySetting, Plan, RegistrationLinkLogs
from common_app.responses import CustomResponse
from common_app.decrypt_string import DecryptString
from common_app.common_function import CommonFunction

logger = logging.getLogger(__name__)


def to_float(val: Any) -> float:
    if val is None or val == "":
        return 0.0
    try:
        return float(val)
    except (ValueError, TypeError):
        return 0.0


def to_int(val: Any) -> Optional[int]:
    if val is None or val == "":
        return None
    try:
        return int(val)
    except (ValueError, TypeError):
        return None


def serialize_country_settings_detail(cs: CountrySetting) -> Dict[str, Any]:
    """Serializes a CountrySetting object to a detailed dictionary, removing None values."""
    expiry_dt_str: Optional[str] = None
    try:
        if cs.cntyLinkExpiryDateTime:
            dt_str = cs.cntyLinkExpiryDateTime.strftime("%Y-%m-%d %H:%M:%S")
            converted = CommonFunction.convertEventTimeZoneToUserDB(dt_str, "UTC", "America/Los_Angeles")
            expiry_dt_str = CommonFunction.displayDateTime(converted)
    except Exception:
        pass

    update_dt_str: Optional[str] = None
    try:
        if cs.cntyUpdateDateTime:
            dt_str = cs.cntyUpdateDateTime.strftime("%Y-%m-%d %H:%M:%S")
            converted = CommonFunction.convertEventTimeZoneToUserDB(dt_str, "UTC", "America/Los_Angeles")
            update_dt_str = CommonFunction.displayDateTime(converted)
    except Exception:
        pass

    raw_dto = {
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
        "cntyLinkExpiryDateTime": expiry_dt_str,
        "cntyUpdateDateTime": update_dt_str,
    }
    return {k: v for k, v in raw_dto.items() if v is not None}


@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_country_settings_by_id(request: Request, countrySettingsId: int) -> CustomResponse:
    """Fetches country setting details by ID."""
    res_body: Dict[str, Any] = {}
    try:
        cs = CountrySetting.objects.filter(id=countrySettingsId).first()
        if cs:
            res_body["countrySettingsById"] = serialize_country_settings_detail(cs)
        else:
            res_body["countrySettingsById"] = None
        return CustomResponse(data=res_body, status=200, message="Country Settings fetched successfully")
    except Exception as e:
        logger.error(f"get_country_settings_by_id error: {e}", exc_info=True)
        return CustomResponse(data=res_body, status=500, message="Country Settings not found ")


@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_country_settings_list_page(request: Request) -> CustomResponse:
    """Lists country settings with search capability and pagination metrics."""
    res_body: Dict[str, Any] = {}
    try:
        search_key = request.query_params.get("searchKey", "")
        page = int(request.query_params.get("page", 0))
        size = int(request.query_params.get("size", 10))

        offset = page * size
        limit = offset + size

        base_query = CountrySetting.objects.all().order_by('id')
        if search_key:
            base_query = base_query.filter(cntyName__icontains=search_key)

        total_records = CountrySetting.objects.count()
        filtered_count = base_query.count()
        total_pages = math.ceil(filtered_count / size) if size > 0 else 0

        paginated_settings = base_query[offset:limit]
        country_setting_dtos = []

        for cs in paginated_settings:
            plan = Plan.objects.filter(planId=cs.cntyPlanId).first()
            plan_name = plan.planName if plan else None
            plan_visibility = plan.planVisibility if plan else None
            enc_plan_id = (
                DecryptString.setEncDecUser(str(plan.planId), "", "Y")
                if plan and plan.planId is not None
                else None
            )

            expiry_dt_str: Optional[str] = None
            try:
                if cs.cntyLinkExpiryDateTime:
                    dt_str = cs.cntyLinkExpiryDateTime.strftime("%Y-%m-%d %H:%M:%S")
                    converted = CommonFunction.convertEventTimeZoneToUserDB(dt_str, "UTC", "America/Los_Angeles")
                    expiry_dt_str = CommonFunction.displayDateTime(converted)
            except Exception:
                pass

            update_dt_str: Optional[str] = None
            try:
                if cs.cntyUpdateDateTime:
                    dt_str = cs.cntyUpdateDateTime.strftime("%Y-%m-%d %H:%M:%S")
                    converted = CommonFunction.convertEventTimeZoneToUserDB(dt_str, "UTC", "America/Los_Angeles")
                    update_dt_str = CommonFunction.displayDateTime(converted)
            except Exception:
                pass

            dto = {
                "id": cs.id,
                "cntyId": cs.cntyId,
                "cntyISO2": cs.cntyISO2,
                "cntyName": cs.cntyName,
                "cntyPriceSymbol": cs.cntyPriceSymbol,
                "cntyPlanPrice": cs.cntyPlanPrice,
                "planName": plan_name,
                "cntyPlanPopular": cs.cntyPlanPopular,
                "planVisibility": plan_visibility,
                "encPlanId": enc_plan_id,
                "cntyLinkExpiryDateTime": expiry_dt_str,
                "cntyUpdateDateTime": update_dt_str,
            }
            country_setting_dtos.append(dto)

        res_body["getTotalPages"] = total_pages
        res_body["getNumber"] = page
        res_body["getSize"] = size
        res_body["countrySettingsListPage"] = country_setting_dtos
        res_body["getTotalRecords"] = total_records

        return CustomResponse(data=res_body, status=200, message="Fetch Country Settings Successfully")
    except Exception as e:
        logger.error(f"get_country_settings_list_page error: {e}", exc_info=True)
        return CustomResponse(data=res_body, status=500, message="error")


@api_view(['POST'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def save_country_settings(request: Request) -> CustomResponse:
    """Creates or updates country settings config."""
    res_body: Dict[str, Any] = {"error": ""}
    current_display_order = 0

    try:
        dto_id = to_int(request.data.get("id")) or 0
        cnty_id = to_int(request.data.get("cntyId"))
        cnty_plan_id = to_int(request.data.get("cntyPlanId"))
        display_order = to_int(request.data.get("cntyPlanDisplayOrder"))

        if dto_id == 0:
            country_setting = CountrySetting.objects.filter(cntyId=cnty_id, cntyPlanId=cnty_plan_id).first()
            if display_order is None or display_order == 0:
                max_order = CountrySetting.objects.filter(cntyId=cnty_id).aggregate(Max('cntyPlanDisplayOrder'))['cntyPlanDisplayOrder__max']
                temp_max_display_order = max_order if max_order is not None else 0
                temp_max_display_order += 1
                display_order = temp_max_display_order
        else:
            country_setting = CountrySetting.objects.filter(cntyId=cnty_id, cntyPlanId=cnty_plan_id).exclude(id=dto_id).first()
            existing_record = CountrySetting.objects.filter(id=dto_id).first()
            if existing_record:
                current_display_order = existing_record.cntyPlanDisplayOrder or 0

        if country_setting is None:
            # Handle timezone conversions for the link expiry date
            link_expiry_str = request.data.get("cntyLinkExpiryDateTime")
            expiry_datetime = None
            if link_expiry_str:
                try:
                    db_dt = CommonFunction.dbDateTime(link_expiry_str)
                    utc_dt_str = CommonFunction.convertEventTimeZoneToUserDB(db_dt, "America/Los_Angeles", "UTC")
                    expiry_datetime = CommonFunction.convertDate(utc_dt_str)
                except Exception:
                    pass

            with transaction.atomic():
                if dto_id == 0:
                    cs = CountrySetting()
                else:
                    cs = CountrySetting.objects.filter(id=dto_id).first()
                    if not cs:
                        cs = CountrySetting()

                cs.cntyId = cnty_id
                cs.cntyISO2 = request.data.get("cntyISO2")
                cs.cntyName = request.data.get("cntyName")
                cs.cntyPriceSymbol = request.data.get("cntyPriceSymbol")
                cs.cntyAssessmentPrice = to_float(request.data.get("cntyAssessmentPrice"))
                cs.cntySurveyPrice = to_float(request.data.get("cntySurveyPrice"))
                cs.cntyIndividualPrice = to_float(request.data.get("cntyIndividualPrice"))
                cs.cntySocialMediaPrice = to_float(request.data.get("cntySocialMediaPrice"))
                cs.cntyCampaignPerPrice = to_float(request.data.get("cntyCampaignPerPrice"))
                cs.cntySurveyPerPrice = to_float(request.data.get("cntySurveyPerPrice"))
                cs.cntyAssessmentPerPrice = to_float(request.data.get("cntyAssessmentPerPrice"))
                cs.cntyMMSPerPrice = to_float(request.data.get("cntyMMSPerPrice"))
                cs.cntySMSPerPrice = to_float(request.data.get("cntySMSPerPrice"))
                cs.cntySMSNumberPerPrice = to_float(request.data.get("cntySMSNumberPerPrice"))
                cs.cntyFirstInvFreeAmt = to_float(request.data.get("cntyFirstInvFreeAmt"))
                cs.cntyInvLessAmtNotCharge = to_float(request.data.get("cntyInvLessAmtNotCharge"))
                cs.cntyTranslateCharCharge = to_float(request.data.get("cntyTranslateCharCharge"))
                cs.cntySMSConversationsPerPrice = to_float(request.data.get("cntySMSConversationsPerPrice"))
                cs.cntyCallPerMinPrice = to_float(request.data.get("cntyCallPerMinPrice"))
                cs.cntyContactsIncluded = to_int(request.data.get("cntyContactsIncluded"))
                cs.cntyMaxNumberOfEmail = to_int(request.data.get("cntyMaxNumberOfEmail"))
                cs.cntyPlanId = cnty_plan_id
                cs.cntyPlanPrice = to_float(request.data.get("cntyPlanPrice"))
                cs.cntySupport = request.data.get("cntySupport")
                cs.cntyMultiUser = request.data.get("cntyMultiUser")
                cs.cntyAutomation = request.data.get("cntyAutomation")
                cs.cntyWhiteListing = request.data.get("cntyWhiteListing")
                cs.cntyCalendar = request.data.get("cntyCalendar")
                cs.cntyZoomConferences = request.data.get("cntyZoomConferences")
                cs.cntySocialMedia = request.data.get("cntySocialMedia")
                cs.cntySmsInbox = request.data.get("cntySmsInbox")
                cs.cntyAbTesting = request.data.get("cntyAbTesting")
                cs.cntyPlanPopular = request.data.get("cntyPlanPopular")
                cs.cntyPlanDisplayOrder = display_order
                cs.cntyFormResponse = to_float(request.data.get("cntyFormResponse"))
                cs.cntyAdditionalContacts = to_int(request.data.get("cntyAdditionalContacts"))
                cs.cntyAdditionalContactsPrice = to_float(request.data.get("cntyAdditionalContactsPrice"))
                cs.cnty10DLCPrice = to_float(request.data.get("cnty10DLCPrice"))
                cs.cnty10DLCCampaignTypeCharge = to_float(request.data.get("cnty10DLCCampaignTypeCharge"))
                cs.cnty10DLCOtherCharge = to_float(request.data.get("cnty10DLCOtherCharge"))
                cs.cntyWarmupPrice = to_float(request.data.get("cntyWarmupPrice"))
                cs.ctnyAiGeneratedImage = to_float(request.data.get("ctnyAiGeneratedImage"))
                cs.ctnyAiEditedImage = to_float(request.data.get("ctnyAiEditedImage"))
                cs.ctnyContactPerPrice = to_float(request.data.get("ctnyContactPerPrice"))
                cs.cntyLinkExpiryDateTime = expiry_datetime
                cs.cntyUpdateDateTime = timezone.now()
                cs.save()

                # Save RegistrationLinkLogs
                try:
                    main_web_app_url = getattr(settings, 'MAIN_WEB_APP_URL', 'https://webapp.salesandmarketing.ai/')
                    lnk_link = f"{main_web_app_url}register?v={DecryptString.setEncDecUser(str(cs.cntyPlanId), '', 'Y')}"
                    log_entry = RegistrationLinkLogs(
                        lnkCountrySettingId=cs.id,
                        lnkPlanId=cs.cntyPlanId,
                        lnkLink=lnk_link,
                        lnkExpiryDateTime=cs.cntyLinkExpiryDateTime,
                        lnkDateTime=timezone.now()
                    )
                    log_entry.save()
                except Exception as ee:
                    logger.error(f"saveCountrySettings log entry error: {ee}", exc_info=True)

                # Set popularity of other plans for the same country to 'N'
                try:
                    CountrySetting.objects.filter(cntyId=cs.cntyId).exclude(cntyPlanId=cs.cntyPlanId).update(cntyPlanPopular='N')
                except Exception as ee:
                    logger.error(f"saveCountrySettings update popularity error: {ee}", exc_info=True)

                # Update display order of previous entity if swapping/oldId is present
                try:
                    old_id = to_int(request.data.get("oldId"))
                    if old_id and old_id > 0:
                        max_order = CountrySetting.objects.filter(cntyId=cs.cntyId).aggregate(Max('cntyPlanDisplayOrder'))['cntyPlanDisplayOrder__max']
                        max_display_order = max_order if max_order is not None else 0
                        max_display_order += 1

                        old_cs = CountrySetting.objects.filter(id=old_id).first()
                        if old_cs:
                            if current_display_order > 0:
                                old_cs.cntyPlanDisplayOrder = current_display_order
                            else:
                                old_cs.cntyPlanDisplayOrder = max_display_order
                            old_cs.save()
                except Exception as ee:
                    logger.error(f"saveCountrySettings display order swap error: {ee}", exc_info=True)

            return CustomResponse(data=res_body, status=200, message="Country Settings Saved Successfully")
        else:
            res_body["error"] = "Country name already exists"
            return CustomResponse(data=res_body, status=500, message=res_body["error"])

    except Exception as e:
        logger.error(f"save_country_settings error: {e}", exc_info=True)
        res_body["error"] = "error"
        return CustomResponse(data=res_body, status=500, message="Country Settings Saved Fail")


@api_view(['DELETE'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_country_settings(request: Request) -> CustomResponse:
    """Bulk deletes country settings."""
    res_body: Dict[str, Any] = {}
    try:
        ids = request.data.get("ids", [])
        if not ids:
            ids = request.data.get("Ids", [])

        if ids:
            CountrySetting.objects.filter(id__in=ids).delete()

        return CustomResponse(data=res_body, status=200, message="Country Settings deleted successfully.")
    except Exception as e:
        logger.error(f"delete_country_settings error: {e}", exc_info=True)
        return CustomResponse(data=res_body, status=500, message="Country Settings delete fail")


@api_view(['POST'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def check_display_order(request: Request) -> CustomResponse:
    """Validates if display order exists for a country."""
    res_body: Dict[str, Any] = {}
    try:
        dto_id = to_int(request.data.get("id")) or 0
        cnty_id = to_int(request.data.get("cntyId"))
        display_order = to_int(request.data.get("cntyPlanDisplayOrder"))

        if dto_id == 0:
            country_setting = CountrySetting.objects.filter(cntyId=cnty_id, cntyPlanDisplayOrder=display_order).first()
        else:
            country_setting = CountrySetting.objects.filter(cntyId=cnty_id, cntyPlanDisplayOrder=display_order).exclude(id=dto_id).first()

        old_id = country_setting.id if country_setting else 0
        res_body["oldId"] = old_id

        return CustomResponse(data=res_body, status=200, message="Check display order successfully")
    except Exception as e:
        logger.error(f"check_display_order error: {e}", exc_info=True)
        return CustomResponse(data=res_body, status=500, message="Check display order fail")


@api_view(['POST'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def add_expiry_date(request: Request) -> CustomResponse:
    """Updates registration link expiry date for country setting."""
    res_body: Dict[str, Any] = {}
    try:
        dto_id = to_int(request.data.get("id"))
        link_expiry_str = request.data.get("cntyLinkExpiryDateTime")

        country_setting = CountrySetting.objects.filter(id=dto_id).first()
        if country_setting:
            expiry_datetime = country_setting.cntyLinkExpiryDateTime
            if link_expiry_str:
                try:
                    db_dt = CommonFunction.dbDateTime(link_expiry_str)
                    utc_dt_str = CommonFunction.convertEventTimeZoneToUserDB(db_dt, "America/Los_Angeles", "UTC")
                    expiry_datetime = CommonFunction.convertDate(utc_dt_str)
                except Exception:
                    pass

            with transaction.atomic():
                country_setting.cntyLinkExpiryDateTime = expiry_datetime
                country_setting.cntyUpdateDateTime = timezone.now()
                country_setting.save()

                try:
                    main_web_app_url = getattr(settings, 'MAIN_WEB_APP_URL', 'https://webapp.salesandmarketing.ai/')
                    lnk_link = f"{main_web_app_url}register?v={DecryptString.setEncDecUser(str(country_setting.cntyPlanId), '', 'Y')}"
                    log_entry = RegistrationLinkLogs(
                        lnkCountrySettingId=country_setting.id,
                        lnkPlanId=country_setting.cntyPlanId,
                        lnkLink=lnk_link,
                        lnkExpiryDateTime=country_setting.cntyLinkExpiryDateTime,
                        lnkDateTime=timezone.now()
                    )
                    log_entry.save()
                except Exception as ee:
                    logger.error(f"add_expiry_date log entry error: {ee}", exc_info=True)

        return CustomResponse(data=res_body, status=200, message="Add expiry date successfully")
    except Exception as e:
        logger.error(f"add_expiry_date error: {e}", exc_info=True)
        return CustomResponse(data=res_body, status=500, message="Add expiry date fail")


@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_registration_link_logs(request: Request) -> CustomResponse:
    """Fetches log history of registration links for a country setting."""
    res_body: Dict[str, Any] = {}
    try:
        dto_id = to_int(request.query_params.get("id"))
        logs_list = RegistrationLinkLogs.objects.filter(lnkCountrySettingId=dto_id).order_by('-lnkId')

        registration_link_logs_dtos = []
        for log in logs_list:
            expiry_dt_str: Optional[str] = None
            try:
                if log.lnkExpiryDateTime:
                    dt_str = log.lnkExpiryDateTime.strftime("%Y-%m-%d %H:%M:%S")
                    converted = CommonFunction.convertEventTimeZoneToUserDB(dt_str, "UTC", "America/Los_Angeles")
                    expiry_dt_str = CommonFunction.displayDateTime(converted)
            except Exception:
                pass

            date_time_str: Optional[str] = None
            try:
                if log.lnkDateTime:
                    dt_str = log.lnkDateTime.strftime("%Y-%m-%d %H:%M:%S")
                    converted = CommonFunction.convertEventTimeZoneToUserDB(dt_str, "UTC", "America/Los_Angeles")
                    date_time_str = CommonFunction.displayDateTime(converted)
            except Exception:
                pass

            dto = {
                "lnkId": log.lnkId,
                "lnkLink": log.lnkLink,
                "lnkExpiryDateTime": expiry_dt_str,
                "lnkDateTime": date_time_str
            }
            registration_link_logs_dtos.append(dto)

        res_body["registrationLinkLogs"] = registration_link_logs_dtos
        return CustomResponse(data=res_body, status=200, message="Fetch Logs Successfully")
    except Exception as e:
        logger.error(f"get_registration_link_logs error: {e}", exc_info=True)
        return CustomResponse(data=res_body, status=500, message="error")
