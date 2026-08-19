from common_app.utils import get_tenant_id_by_client_id
import logging
import math
from django.db.models import Count
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated

from auth_app.authentication import CustomJWTAuthentication
from common_app.models import (
    Tenants, CampaignsEmailSend, CampaignsSendEmail, CampaignsSendEmailArchive,
    CampaignLinks, CampaignLinkClick, CampaignSubscriber, Group, Userlist
)
from common_app.utils import *
from common_app.responses import CustomResponse
from common_app.common_function import CommonFunction
from common_app.decrypt_string import DecryptString

logger = logging.getLogger(__name__)


@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_email_campaigns_report_list_page(request: Request) -> CustomResponse:
    res_body = {}
    try:
        search_key = request.query_params.get("searchKey", "")
        page = int(request.query_params.get("page", 0))
        size = int(request.query_params.get("size", 10))
        camp_id_param = request.query_params.get("id")
        member_id_param = request.query_params.get("memberId")
        time_zone_param = request.query_params.get("timeZone", "")

        if not camp_id_param or not member_id_param:
            return CustomResponse(data=res_body, status=400, message="Missing required parameters")

        camp_id = int(camp_id_param)
        member_id = int(member_id_param)

        member = Tenants.objects.select_related('details').filter(ten_id=get_tenant_id_by_client_id(member_id)).first()
        if not member:
            return CustomResponse(data=res_body, status=404, message="Member not found")

        final_member_id = CommonFunction.getFinalMemberId(member)
        final_member = Tenants.objects.select_related('details').filter(ten_id=final_member_id).first()
        tempt_time_zone = get_client_time_zone(get_client_id_by_tenant_id(final_member_id)) if final_member else None
        if not tempt_time_zone:
            tempt_time_zone = time_zone_param

        offset = page * size
        limit = offset + size

        queryset = CampaignsEmailSend.objects.filter(memberId=get_client_id_by_tenant_id(final_member_id), campId=camp_id).order_by('id')

        if search_key:
            queryset = queryset.filter(campName__icontains=search_key)

        total_pages = math.ceil(queryset.count() / size) if size > 0 else 0
        paginated_campaigns = queryset[offset:limit]

        total_campaigns_email_send = CampaignsEmailSend.objects.filter(memberId=final_member_id, campId=camp_id).count()

        campaigns_email_send_response_dto_list = []
        for campaigns_email_send in paginated_campaigns:
            dto = {
                "campName": campaigns_email_send.campName,
                "campId": campaigns_email_send.id,
            }
            if campaigns_email_send.campMainType is not None:
                dto["campMainType"] = campaigns_email_send.campMainType

            dto["encCampId"] = DecryptString.setEncDecUser(str(campaigns_email_send.id), "", "Y")

            if campaigns_email_send.sendDate:
                dto["createdOn"] = CommonFunction.displayDateTime(str(campaigns_email_send.sendDate))
            if campaigns_email_send.sendOnDate:
                dto["sendOnDate"] = CommonFunction.convertEventTimeZoneToUser(
                    CommonFunction.displayDateTime(str(campaigns_email_send.sendOnDate)), "UTC", tempt_time_zone
                )

            campaigns_email_send_response_dto_list.append(dto)

        res_body["getTotalPages"] = total_pages
        res_body["getNumber"] = page
        res_body["getSize"] = size
        res_body["totalCampaignsEmailSend"] = total_campaigns_email_send
        res_body["emailCampaignsReportList"] = campaigns_email_send_response_dto_list

        return CustomResponse(data=res_body, status=200, message="Email Campaigns Fetched Successfully")
    except Exception as e:
        logger.error(f"[ memberId : {request.query_params.get('memberId')} ] GetEmailCampaignsReportListPage Error : {e}", exc_info=True)
        return CustomResponse(data=res_body, status=500, message="error")


@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_email_campaigns_report_dashboard(request: Request) -> CustomResponse:
    res_body = {}
    dashboard = {}
    try:
        member_id_param = request.query_params.get("memberId")
        camp_id_encrypted = request.query_params.get("campId")
        time_zone_param = request.query_params.get("timeZone", "")

        if not member_id_param or not camp_id_encrypted:
            return CustomResponse(data=res_body, status=400, message="Missing required parameters")

        member_id = int(member_id_param)
        dec_camp_id = int(DecryptString.setEncDecUser(camp_id_encrypted, "display", "Y"))

        member = Tenants.objects.select_related('details').filter(memberId=get_tenant_id_by_client_id(member_id)).first()
        if not member:
            return CustomResponse(data=res_body, status=404, message="Member not found")

        final_member_id = CommonFunction.getFinalMemberId(member)
        final_member = Tenants.objects.select_related('details').filter(ten_id=final_member_id).first()
        tempt_time_zone = get_client_time_zone(get_client_id_by_tenant_id(final_member_id)) if final_member else None
        if not tempt_time_zone:
            tempt_time_zone = time_zone_param

        campaigns_email_send = CampaignsEmailSend.objects.filter(id=dec_camp_id).first()
        if not campaigns_email_send:
            return CustomResponse(data=res_body, status=404, message="Campaign not found")

        dashboard["campName"] = campaigns_email_send.campName

        if campaigns_email_send.sendOnDate:
            dashboard["sentOn"] = CommonFunction.convertEventTimeZoneToUser(
                CommonFunction.displayDateTime(str(campaigns_email_send.sendOnDate)), "UTC", tempt_time_zone
            )

        group_name = ""
        if campaigns_email_send.groupList:
            try:
                group_id_val = int(campaigns_email_send.groupList)
                group_obj = Group.objects.filter(groupId=group_id_val).first()
                if group_obj:
                    group_name = group_obj.groupName
            except ValueError:
                pass

        dashboard["mailingGroup"] = group_name
        dashboard["subject"] = campaigns_email_send.subject
        dashboard["senderName"] = campaigns_email_send.fromName
        dashboard["senderEmail"] = campaigns_email_send.fromAdd

        sent = CampaignsSendEmail.objects.filter(campSendId=dec_camp_id).count()
        dashboard["sent"] = sent

        deliveries = CampaignsSendEmail.objects.filter(campSendId=dec_camp_id, isSend='Y').count()
        dashboard["delivered"] = deliveries

        opened = CampaignsSendEmail.objects.filter(campSendId=dec_camp_id, isRead='Y').count()
        dashboard["opened"] = opened

        bounced = CampaignsSendEmail.objects.filter(campSendId=dec_camp_id, isBounced='Y').count()
        dashboard["bounced"] = bounced

        unsubscribed = CampaignsSendEmail.objects.filter(campSendId=dec_camp_id, isUnsubscribed='Y').count()
        unread = deliveries - opened
        dashboard["unread"] = unread

        link_count_total = 0
        ui = 0
        total_desktop = 0
        total_mobile = 0

        campaign_links_list = CampaignLinks.objects.filter(campId=dec_camp_id).order_by('id')
        for cll in campaign_links_list:
            link_count_total += cll.linkCount or 0

            pc = CampaignLinkClick.objects.filter(linkId=cll.id, sources='PC').count()
            total_desktop += pc

            phone = CampaignLinkClick.objects.filter(linkId=cll.id, sources='Phone').count()
            total_mobile += phone

            tc_count = CampaignLinkClick.objects.filter(linkId=cll.id).values('userId').distinct().count()
            ui += tc_count

        successful_deliveries = deliveries
        successful_deliveries_per = 0.0
        if sent > 0:
            successful_deliveries_per = (successful_deliveries / sent) * 100

        dashboard["totalDesktop"] = total_desktop
        dashboard["totalMobile"] = total_mobile
        dashboard["successfulDeliveries"] = successful_deliveries
        dashboard["successfulDeliveriesPer"] = successful_deliveries_per

        bounced_per = 0.0
        if sent > 0:
            bounced_per = (bounced * 100) / sent
        dashboard["bouncedPer"] = bounced_per

        unsubscribed_per = 0.0
        if sent > 0:
            unsubscribed_per = (unsubscribed * 100) / sent
        dashboard["unsubscribed"] = unsubscribed
        dashboard["unsubscribedPer"] = unsubscribed_per

        open_rate_per = 0.0
        if successful_deliveries > 0:
            open_rate_per = (opened * 100) / successful_deliveries
        dashboard["openRatePer"] = open_rate_per

        total_click_through_rate_per = 0.0
        if deliveries > 0:
            total_click_through_rate_per = (link_count_total * 100) / deliveries
        dashboard["totalClickThroughRate"] = link_count_total
        dashboard["totalClickThroughRatePer"] = total_click_through_rate_per

        unique_click_through_rate_per = 0.0
        if successful_deliveries > 0:
            unique_click_through_rate_per = (ui * 100) / successful_deliveries
        dashboard["uniqueClickThroughRate"] = ui
        dashboard["uniqueClickThroughRatePer"] = unique_click_through_rate_per

        if campaigns_email_send.lastOpened:
            dashboard["lastOpened"] = CommonFunction.displayDateTime(str(campaigns_email_send.lastOpened))

        res_body["dashboard"] = dashboard
        return CustomResponse(data=res_body, status=200, message="Email Campaigns Dashboard Fetched Successfully")
    except Exception as e:
        logger.error(f"[ memberId : {request.query_params.get('memberId')} ] GetEmailCampaignsReportDashboard Error : {e}", exc_info=True)
        return CustomResponse(data=res_body, status=500, message="error")


@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_bounced_email_report_list(request: Request) -> CustomResponse:
    res_body = {}
    try:
        camp_send_id_encrypted = request.query_params.get("campSendId")
        split_group = request.query_params.get("splitGroup", "")

        if not camp_send_id_encrypted:
            return CustomResponse(data=res_body, status=400, message="Missing campSendId")

        dec_camp_id = int(DecryptString.setEncDecUser(camp_send_id_encrypted, "display", "Y"))

        queryset = CampaignsSendEmailArchive.objects.filter(campSendId=dec_camp_id, isBounced='Y')
        if split_group:
            queryset = queryset.filter(splitGroup=split_group)

        bounced_email_list = []
        for campaigns_send_email in queryset:
            dto = {}
            if campaigns_send_email.firstName and campaigns_send_email.firstName != "null":
                dto["firstName"] = campaigns_send_email.firstName
            if campaigns_send_email.lastName and campaigns_send_email.lastName != "null":
                dto["lastName"] = campaigns_send_email.lastName
            if campaigns_send_email.email and campaigns_send_email.email != "null":
                dto["email"] = DecryptString.setEncDecUser(campaigns_send_email.email, "display", "Y")
            bounced_email_list.append(dto)

        res_body["bouncedEmailList"] = bounced_email_list
        return CustomResponse(data=res_body, status=200, message="Fetched Bounced Email List Successfully")
    except Exception as e:
        logger.error(f"GetBouncedEmailReportList Error : {e}", exc_info=True)
        return CustomResponse(data=res_body, status=500, message="error")


@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_email_campaigns_report_product_links(request: Request) -> CustomResponse:
    res_body = {}
    product_link_response_dto_list = []
    res_body["productLinks"] = product_link_response_dto_list
    try:
        camp_id_encrypted = request.query_params.get("campId")
        id_param = request.query_params.get("id")

        if not camp_id_encrypted:
            return CustomResponse(data=res_body, status=400, message="Missing campId")

        dec_camp_id = int(DecryptString.setEncDecUser(camp_id_encrypted, "display", "Y"))

        total_recept = CampaignsSendEmail.objects.filter(campSendId=dec_camp_id, isSend='Y').count()

        campaign_links_list = CampaignLinks.objects.filter(campId=dec_camp_id).order_by('id')
        for cll in campaign_links_list:
            click_through = 0.0
            if total_recept > 0:
                click_through = (cll.linkCount / total_recept) * 100

            uc = CampaignLinkClick.objects.filter(linkId=cll.id).values('userId').distinct().count()

            product_link_response_dto = {
                "id": cll.id,
                "campLink": cll.campLink,
                "uniqueClicks": uc,
                "totalClicks": cll.linkCount,
                "clickThroughRate": click_through,
                "userDetailList": []
            }

            user_wise_clicks = CampaignLinkClick.objects.filter(linkId=cll.id).values('userId').annotate(linkCount=Count('userId')).order_by()
            for arow2 in user_wise_clicks:
                user_id = arow2['userId']
                if user_id is None:
                    continue

                click_user_detail = CampaignsSendEmailArchive.objects.filter(emailId=user_id).order_by('-id').first()

                first_name = ""
                last_name = ""
                if click_user_detail:
                    first_name = click_user_detail.firstName or ""
                    last_name = click_user_detail.lastName or ""

                user_name = f"{first_name} {last_name}".strip()

                link_detail_user_wise = {
                    "userId": user_id,
                    "userName": user_name,
                    "totalClicked": arow2['linkCount'],
                    "locationList": []
                }

                campaign_links_detail_list = CampaignLinkClick.objects.filter(linkId=cll.id, userId=user_id)
                for arow3 in campaign_links_detail_list:
                    click_date = ""
                    if arow3.clickDate:
                        click_date = CommonFunction.displayDateTime(str(arow3.clickDate))

                    sources = ""
                    if arow3.sources == "PC":
                        sources = "Desktop"
                    elif arow3.sources == "Phone":
                        sources = "Mobile"

                    city = arow3.city
                    browser = CommonFunction.getBrowserName(arow3.sourceDetails)

                    click_location_dto = {
                        "location": city,
                        "clickDate": click_date,
                        "browser": browser,
                        "technology": sources
                    }
                    link_detail_user_wise["locationList"].append(click_location_dto)

                product_link_response_dto["userDetailList"].append(link_detail_user_wise)

            product_link_response_dto_list.append(product_link_response_dto)

        res_body["productLinks"] = product_link_response_dto_list
        return CustomResponse(data=res_body, status=200, message="Email Campaigns Product Links Fetched Successfully")
    except Exception as e:
        logger.error(f"[ campId : {request.query_params.get('campId')} ] GetEmailCampaignsReportProductLinks Error : {e}", exc_info=True)
        return CustomResponse(data=res_body, status=500, message="error")


@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_email_campaigns_report_product_links_click_user(request: Request) -> CustomResponse:
    res_body = {}
    product_links_click_user_list = []
    res_body["productLinksClickUser"] = product_links_click_user_list
    try:
        link_id_param = request.query_params.get("linkId")
        if not link_id_param:
            return CustomResponse(data=res_body, status=400, message="Missing linkId")

        link_id = int(link_id_param)

        user_wise_clicks = CampaignLinkClick.objects.filter(linkId=link_id).values('userId').annotate(linkCount=Count('userId')).order_by()
        for lc in user_wise_clicks:
            user_id = lc['userId']
            if user_id is None:
                continue

            click_user_detail = CampaignsSendEmailArchive.objects.filter(emailId=user_id).order_by('-id').first()
            first_name = ""
            last_name = ""
            if click_user_detail:
                first_name = click_user_detail.firstName or ""
                last_name = click_user_detail.lastName or ""

            user_name = f"{first_name} {last_name}".strip()

            product_links_click_user_list.append({
                "userName": user_name,
                "linkCount": lc['linkCount']
            })

        res_body["productLinksClickUser"] = product_links_click_user_list
        return CustomResponse(data=res_body, status=200, message="Email Campaigns Product Links User Click Fetched Successfully")
    except Exception as e:
        logger.error(f"[ linkId : {request.query_params.get('linkId')} ] GetEmailCampaignsReportProductLinksClickUser Error : {e}", exc_info=True)
        return CustomResponse(data=res_body, status=500, message="error")


@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_email_campaigns_report_members_list_page(request: Request) -> CustomResponse:
    res_body = {}
    try:
        member_id_param = request.query_params.get("memberId")
        search_key = request.query_params.get("searchKey", "")
        page = int(request.query_params.get("page", 0))
        size = int(request.query_params.get("size", 10))
        camp_id_encrypted = request.query_params.get("campId")

        if not camp_id_encrypted:
            return CustomResponse(data=res_body, status=400, message="Missing campId")

        dec_camp_id = int(camp_id_encrypted)

        final_member_id = None
        if member_id_param:
            member_id = int(member_id_param)
            member = Tenants.objects.select_related('details').filter(memberId=get_tenant_id_by_client_id(member_id)).first()
            if member:
                final_member_id = CommonFunction.getFinalMemberId(member)

        if final_member_id is None and member_id_param:
            final_member_id = int(member_id_param)

        offset = page * size
        limit = offset + size

        queryset = CampaignsSendEmailArchive.objects.filter(campSendId=dec_camp_id).order_by('id')
        if search_key:
            queryset = queryset.filter(firstName__icontains=search_key)

        total_pages = math.ceil(queryset.count() / size) if size > 0 else 0
        paginated_members = queryset[offset:limit]

        total_campaigns_send_email = CampaignsSendEmail.objects.filter(campSendId=dec_camp_id).count()

        campaigns_send_email_dto_list = []
        for campaigns_send_email in paginated_members:
            email_dec = campaigns_send_email.email

            unsubscribe_date_str = ""
            if final_member_id is not None:
                unsubscribe_user = Userlist.objects.filter(
                    emailId=campaigns_send_email.emailId,
                    memberId=final_member_id,
                    status='Unsubscribed',
                    optId=dec_camp_id
                ).first()
                if unsubscribe_user and unsubscribe_user.optDate:
                    unsubscribe_date_str = CommonFunction.displayDateTime(str(unsubscribe_user.optDate))

            total_open = CampaignSubscriber.objects.filter(campId=dec_camp_id, subId=campaigns_send_email.emailId).count()

            # Count total click
            count_total_click = CampaignLinkClick.objects.filter(
                userId=campaigns_send_email.emailId,
                linkId__in=CampaignLinks.objects.filter(campId=dec_camp_id).values_list('id', flat=True)
            ).count()

            link_info_list = []
            if count_total_click > 0:
                campaign_links_list = CampaignLinks.objects.filter(campId=dec_camp_id).order_by('id')
                for campaign_links in campaign_links_list:
                    link_clicked = CampaignLinkClick.objects.filter(
                        linkId=campaign_links.id,
                        userId=campaigns_send_email.emailId
                    ).count()
                    link_info_list.append({
                        "link": campaign_links.campLink,
                        "linkClicked": link_clicked
                    })

            campaigns_send_email_dto = {
                "firstName": campaigns_send_email.firstName,
                "lastName": campaigns_send_email.lastName,
                "emailId": campaigns_send_email.emailId,
                "email": email_dec,
                "unsubscribeDate": unsubscribe_date_str,
                "totalOpen": total_open,
                "countTotalClick": count_total_click,
                "linkDetail": link_info_list
            }
            campaigns_send_email_dto_list.append(campaigns_send_email_dto)

        res_body["getTotalPages"] = total_pages
        res_body["getNumber"] = page
        res_body["getSize"] = size
        res_body["totalCampaignsSendEmail"] = total_campaigns_send_email
        res_body["emailCampaignsReportMembers"] = campaigns_send_email_dto_list

        return CustomResponse(data=res_body, status=200, message="Email Campaigns Member List Fetched Successfully")
    except Exception as e:
        logger.error(f"[ memberId : {request.query_params.get('memberId')} ] GetEmailCampaignsReportMembers Error : {e}", exc_info=True)
        return CustomResponse(data=res_body, status=500, message="error")


@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_email_campaigns_report_member_click(request: Request) -> CustomResponse:
    res_body = {}
    product_links_list = []
    res_body["productLinks"] = product_links_list
    product_link_response_dto_list = []
    res_body["technology"] = product_link_response_dto_list
    locations = []
    res_body["location"] = locations
    try:
        email_id_param = request.query_params.get("emailId")
        camp_id_encrypted = request.query_params.get("campId")

        if not email_id_param or not camp_id_encrypted:
            return CustomResponse(data=res_body, status=400, message="Missing emailId or campId")

        email_id = int(email_id_param)
        dec_camp_id = int(DecryptString.setEncDecUser(camp_id_encrypted, "display", "Y"))

        total_open = CampaignSubscriber.objects.filter(campId=dec_camp_id, subId=email_id).count()
        res_body["totalEmailOpen"] = total_open

        campaign_links_list = CampaignLinks.objects.filter(campId=dec_camp_id).order_by('id')
        for campaign_links in campaign_links_list:
            link_clicked = CampaignLinkClick.objects.filter(linkId=campaign_links.id, userId=email_id).count()
            product_links_list.append({
                "link": campaign_links.campLink,
                "linkClicked": link_clicked
            })

            # Technology
            pc = CampaignLinkClick.objects.filter(linkId=campaign_links.id, sources='PC', userId=email_id).count()
            phone = CampaignLinkClick.objects.filter(linkId=campaign_links.id, sources='Phone', userId=email_id).count()

            product_link_response_dto_list.append({
                "id": campaign_links.id,
                "campLink": campaign_links.campLink,
                "clickThroughRate": None,
                "pc": pc,
                "mobile": phone
            })

            # Location
            campaign_links_detail_list = CampaignLinkClick.objects.filter(linkId=campaign_links.id, userId=email_id)
            for campaign_link_click in campaign_links_detail_list:
                click_date = ""
                if campaign_link_click.clickDate:
                    click_date = CommonFunction.displayDateTime(str(campaign_link_click.clickDate))

                city = campaign_link_click.city
                browser = CommonFunction.getBrowserName(campaign_link_click.sourceDetails)

                locations.append({
                    "link": campaign_links.campLink,
                    "location": city,
                    "date": click_date,
                    "browser": browser
                })

        res_body["productLinks"] = product_links_list
        res_body["technology"] = product_link_response_dto_list
        res_body["location"] = locations

        return CustomResponse(data=res_body, status=200, message="Email Campaigns Member Information Fetched Successfully")
    except Exception as e:
        logger.error(f"[ emailId : {request.query_params.get('emailId')} ] GetEmailCampaignsReportMembersClick Error : {e}", exc_info=True)
        return CustomResponse(data=res_body, status=500, message="error")


@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_email_campaigns_report_members_list(request: Request) -> CustomResponse:
    res_body = {}
    campaigns_send_email_dto_list = []
    res_body["members"] = campaigns_send_email_dto_list
    try:
        member_id_param = request.query_params.get("memberId")
        camp_id_encrypted = request.query_params.get("campId")

        if not member_id_param or not camp_id_encrypted:
            return CustomResponse(data=res_body, status=400, message="Missing memberId or campId")

        member_id = int(member_id_param)
        dec_camp_id = int(camp_id_encrypted)

        member = Tenants.objects.select_related('details').filter(memberId=get_tenant_id_by_client_id(member_id)).first()
        final_member_id = CommonFunction.getFinalMemberId(member) if member else member_id

        camp_name_val = CampaignsEmailSend.objects.filter(id=dec_camp_id).values_list('campName', flat=True).first()
        res_body["campName"] = camp_name_val or ""

        campaigns_email_send_list = CampaignsSendEmailArchive.objects.filter(campSendId=dec_camp_id).order_by('firstName')
        for campaigns_send_email in campaigns_email_send_list:
            email_dec = campaigns_send_email.email

            unsubscribe_date_str = ""
            unsubscribe_user = Userlist.objects.filter(
                emailId=campaigns_send_email.emailId,
                memberId=final_member_id,
                status='Unsubscribed',
                optId=dec_camp_id
            ).first()
            if unsubscribe_user and unsubscribe_user.optDate:
                unsubscribe_date_str = CommonFunction.displayDateTime(str(unsubscribe_user.optDate))

            total_open = CampaignSubscriber.objects.filter(campId=dec_camp_id, subId=campaigns_send_email.emailId).count()

            campaigns_send_email_dto_list.append({
                "firstName": campaigns_send_email.firstName,
                "lastName": campaigns_send_email.lastName,
                "emailId": campaigns_send_email.emailId,
                "email": email_dec,
                "unsubscribeDate": unsubscribe_date_str,
                "totalOpen": total_open
            })

        res_body["members"] = campaigns_send_email_dto_list
        return CustomResponse(data=res_body, status=200, message="Email Campaigns Member List Fetched Successfully")
    except Exception as e:
        logger.error(f"[ memberId : {request.query_params.get('memberId')} ] GetEmailCampaignsReportMembersList Error : {e}", exc_info=True)
        return CustomResponse(data=res_body, status=500, message="error")


@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_email_campaigns_report_sources(request: Request) -> CustomResponse:
    res_body = {}
    product_link_response_dto_list = []
    res_body["emailCampaignsReportSourceLinks"] = product_link_response_dto_list
    try:
        camp_id_encrypted = request.query_params.get("campId")
        id_param = request.query_params.get("id")

        if not camp_id_encrypted:
            return CustomResponse(data=res_body, status=400, message="Missing campId")

        dec_camp_id = int(DecryptString.setEncDecUser(camp_id_encrypted, "display", "Y"))

        campaign_links_list = CampaignLinks.objects.filter(campId=dec_camp_id).order_by('id')
        for cll in campaign_links_list:
            pc = CampaignLinkClick.objects.filter(linkId=cll.id, sources='PC').count()
            phone = CampaignLinkClick.objects.filter(linkId=cll.id, sources='Phone').count()

            product_link_response_dto_list.append({
                "id": cll.id,
                "campLink": cll.campLink,
                "clickThroughRate": None,
                "pc": pc,
                "mobile": phone
            })

        res_body["emailCampaignsReportSourceLinks"] = product_link_response_dto_list
        return CustomResponse(data=res_body, status=200, message="Email Campaigns Product Sources Fetched Successfully")
    except Exception as e:
        logger.error(f"[ campId : {request.query_params.get('campId')} ] GetEmailCampaignsReportSources Error : {e}", exc_info=True)
        return CustomResponse(data=res_body, status=500, message="error")


@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_campaigns_report_print(request: Request) -> CustomResponse:
    res_body = {}
    product_link_response_dto_list = []
    res_body["productLinks"] = product_link_response_dto_list
    campaigns_send_email_dto_list = []
    res_body["members"] = campaigns_send_email_dto_list
    source_links_list = []
    res_body["sourceLinks"] = source_links_list
    try:
        member_id_param = request.query_params.get("memberId")
        camp_id_encrypted = request.query_params.get("campId")
        id_param = request.query_params.get("id")

        if not member_id_param or not camp_id_encrypted:
            return CustomResponse(data=res_body, status=400, message="Missing memberId or campId")

        member_id = int(member_id_param)
        dec_camp_id = int(camp_id_encrypted)

        member = Tenants.objects.select_related('details').filter(memberId=get_tenant_id_by_client_id(member_id)).first()
        final_member_id = CommonFunction.getFinalMemberId(member) if member else member_id

        # Product Links
        total_recept = CampaignsSendEmail.objects.filter(campSendId=dec_camp_id, isSend='Y').count()

        campaign_links_list = CampaignLinks.objects.filter(campId=dec_camp_id).order_by('id')
        for cll in campaign_links_list:
            click_through = 0.0
            if total_recept > 0:
                click_through = (cll.linkCount / total_recept) * 100

            uc = CampaignLinkClick.objects.filter(linkId=cll.id).values('userId').distinct().count()

            product_link_response_dto_list.append({
                "id": cll.id,
                "campLink": cll.campLink,
                "uniqueClicks": uc,
                "totalClicks": cll.linkCount,
                "clickThroughRate": click_through
            })

        # Members
        campaigns_email_send_list = CampaignsSendEmailArchive.objects.filter(campSendId=dec_camp_id).order_by('firstName')
        for campaigns_send_email in campaigns_email_send_list:
            email_dec = DecryptString.setEncDecUser(campaigns_send_email.email, "display", "Y")

            unsubscribe_date_str = ""
            unsubscribe_user = Userlist.objects.filter(
                emailId=campaigns_send_email.emailId,
                memberId=final_member_id,
                status='Unsubscribed',
                optId=dec_camp_id
            ).first()
            if unsubscribe_user and unsubscribe_user.optDate:
                unsubscribe_date_str = CommonFunction.displayDateTime(str(unsubscribe_user.optDate))

            total_open = CampaignSubscriber.objects.filter(campId=dec_camp_id, subId=campaigns_send_email.emailId).count()

            campaigns_send_email_dto_list.append({
                "firstName": campaigns_send_email.firstName,
                "lastName": campaigns_send_email.lastName,
                "emailId": campaigns_send_email.emailId,
                "email": email_dec,
                "unsubscribeDate": unsubscribe_date_str,
                "totalOpen": total_open
            })

        # Sources
        for cll in campaign_links_list:
            pc = CampaignLinkClick.objects.filter(linkId=cll.id, sources='PC').count()
            phone = CampaignLinkClick.objects.filter(linkId=cll.id, sources='Phone').count()

            source_links_list.append({
                "id": cll.id,
                "campLink": cll.campLink,
                "clickThroughRate": None,
                "pc": pc,
                "mobile": phone
            })

        res_body["productLinks"] = product_link_response_dto_list
        res_body["members"] = campaigns_send_email_dto_list
        res_body["sourceLinks"] = source_links_list

        return CustomResponse(data=res_body, status=200, message="Email Campaigns Report Print Fetched Successfully")
    except Exception as e:
        logger.error(f"[ memberId : {request.query_params.get('memberId')} ] GetCampaignsReportPrint Error : {e}", exc_info=True)
        return CustomResponse(data=res_body, status=500, message="error")
