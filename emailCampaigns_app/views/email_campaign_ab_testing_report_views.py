import logging
import math
from typing import Any, Dict, List, Optional
from django.db import models as django_models
from django.db.models import Count
from django.utils import timezone
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated

from auth_app.authentication import CustomJWTAuthentication
from common_app.models import (
    Tenants, CampaignsEmailSend, CampaignsSendEmail, CampaignsSendEmailArchive,
    CampaignLinks, CampaignLinkClick, CampaignSubscriber, Group, Userlist,
    SmtpServer, CampaignTransaction, CountrySetting, CampaignsEmail
)
from common_app.utils import *
from common_app.responses import CustomResponse
from common_app.common_function import CommonFunction

logger = logging.getLogger(__name__)


def country_setting_by_member_id(member_id: int) -> Optional[CountrySetting]:
    if member_id > 0:
        member = Tenants.objects.select_related('details').filter(ten_id=member_id).first()
        if member:
            country_id = member.ten_country
            if not country_id:
                country_id = "100"
            plan_id = member.planId
            if plan_id == 0:
                plan_id = 1
            
            country_setting = CountrySetting.objects.filter(cntyId=int(country_id), cntyPlanId=plan_id).first()
            if country_setting:
                return country_setting

    country_setting = CountrySetting.objects.filter(cntyId=100, cntyPlanId=2).first()
    return country_setting


def save_campaign_transaction(
    tran_campaign_id: int,
    tran_campaign_name: str,
    tran_total_member: int,
    tran_type: str,
    tran_invoiced_id: Optional[int],
    tran_invoiced_status: str,
    tran_invoiced_date: Optional[Any],
    member_id: int,
    tran_bill_type: str,
    tran_total_amount: float,
    tran_member_rate: float,
    tran_count_total_sms: int,
    tran_poll_form_no: Optional[str],
    tran_poll_to_no: Optional[str],
    sub_member_id: int
) -> None:
    CampaignTransaction.objects.create(
        tranCampaignId=tran_campaign_id,
        tranCampaignName=tran_campaign_name,
        tranCampaignDate=timezone.now(),
        tranTotalMember=tran_total_member,
        tranType=tran_type,
        tranInvoicedId=tran_invoiced_id,
        tranInvoicedStatus=tran_invoiced_status,
        tranInvoicedDate=tran_invoiced_date,
        memberId=member_id,
        tranBillType=tran_bill_type,
        tranTotalAmount=tran_total_amount,
        tranMemberRate=tran_member_rate,
        tranCountTotalSms=tran_count_total_sms,
        tranPollFormNo=tran_poll_form_no,
        tranPollToNo=tran_poll_to_no,
        subMemberId=sub_member_id
    )


def report_product_links(id_val: int, camp_id: int, split_group: str) -> List[Dict[str, Any]]:
    product_link_response_dto_list = []
    try:
        total_recept = CampaignsSendEmail.objects.filter(campSendId=camp_id, isSend='Y').count()
        campaign_links_list = CampaignLinks.objects.filter(campId=camp_id, splitGroup=split_group).order_by('id')

        for cll in campaign_links_list:
            uc = CampaignLinkClick.objects.filter(linkId=cll.id).values('userId').distinct().count()
            click_through = 0.0
            if total_recept > 0:
                click_through = (cll.linkCount / total_recept) * 100

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

    except Exception as e:
        logger.error(f"[ campId : {camp_id} ] ReportProductLinks Error : {e}", exc_info=True)
    return product_link_response_dto_list


def report_sources(id_val: int, camp_id: int, split_group: str) -> List[Dict[str, Any]]:
    product_link_response_dto_list = []
    try:
        campaign_links_list = CampaignLinks.objects.filter(campId=camp_id, splitGroup=split_group).order_by('id')
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
    except Exception as e:
        logger.error(f"[ campId : {camp_id} ] ReportSources Error : {e}", exc_info=True)
    return product_link_response_dto_list


def print_product_link(final_member_id: int, id_val: int, camp_id: int, split_group: str) -> List[Dict[str, Any]]:
    product_link_response_dto_list = []
    try:
        total_recept = CampaignsSendEmailArchive.objects.filter(
            campSendId=camp_id, splitGroup=split_group, isSend='Y', isBounced='N'
        ).count()
        campaign_links_list = CampaignLinks.objects.filter(campId=camp_id, splitGroup=split_group).order_by('id')
        for cll in campaign_links_list:
            uc = CampaignLinkClick.objects.filter(linkId=cll.id).values('userId').distinct().count()
            click_through = 0.0
            if total_recept > 0:
                click_through = (cll.linkCount / total_recept) * 100

            product_link_response_dto = {
                "id": cll.id,
                "campLink": cll.campLink,
                "uniqueClicks": uc,
                "totalClicks": cll.linkCount,
                "clickThroughRate": click_through
            }
            product_link_response_dto_list.append(product_link_response_dto)
    except Exception as e:
        logger.error(f"[ memberId : {final_member_id} ] PrintProductLink Error : {e}", exc_info=True)
    return product_link_response_dto_list


def print_members(final_member_id: int, id_val: int, camp_id: int, split_group: str) -> List[Dict[str, Any]]:
    campaigns_send_email_dto_list = []
    try:
        campaigns_email_send_list = CampaignsSendEmailArchive.objects.filter(campSendId=camp_id, splitGroup=split_group)
        for campaigns_send_email in campaigns_email_send_list:
            email_dec = campaigns_send_email.email

            unsubscribe_date_str = ""
            unsubscribe_user = Userlist.objects.filter(
                emailId=campaigns_send_email.emailId,
                memberId=final_member_id,
                status='Unsubscribed',
                optId=camp_id
            ).first()
            if unsubscribe_user and unsubscribe_user.optDate:
                unsubscribe_date_str = CommonFunction.displayDateTime(str(unsubscribe_user.optDate))

            total_open = CampaignSubscriber.objects.filter(campId=camp_id, subId=campaigns_send_email.emailId).count()

            campaigns_send_email_dto_list.append({
                "firstName": campaigns_send_email.firstName,
                "lastName": campaigns_send_email.lastName,
                "emailId": campaigns_send_email.emailId,
                "email": email_dec,
                "unsubscribeDate": unsubscribe_date_str,
                "totalOpen": total_open
            })
    except Exception as e:
        logger.error(f"[ memberId : {final_member_id} ] PrintMembers Error : {e}", exc_info=True)
    return campaigns_send_email_dto_list


def print_sources(final_member_id: int, id_val: int, camp_id: int, split_group: str) -> List[Dict[str, Any]]:
    product_link_response_dto_list = []
    try:
        campaign_links_list = CampaignLinks.objects.filter(campId=camp_id, splitGroup=split_group).order_by('id')
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
    except Exception as e:
        logger.error(f"[ memberId : {final_member_id} ] PrintSources Error : {e}", exc_info=True)
    return product_link_response_dto_list


@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_email_campaigns_report_dashboard_ab(request: Request) -> CustomResponse:
    res_body = {}
    dashboard = {}
    dashboard_b = {}
    dashboard_o = {}
    winner = ""
    try:
        member_id_param = request.query_params.get("memberId")
        camp_id_encrypted = request.query_params.get("campId")
        time_zone_param = request.query_params.get("timeZone", "")

        if not member_id_param or not camp_id_encrypted:
            return CustomResponse(data=res_body, status=400, message="Missing required parameters")

        member_id = int(member_id_param)
        dec_camp_id = int(camp_id_encrypted)

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
            return CustomResponse(data=res_body, status=404, message="Campaign send record not found")

        res_body["campName"] = campaigns_email_send.campName
        res_body["resultTie"] = campaigns_email_send.resultTie
        res_body["isCompletedAB"] = campaigns_email_send.isCompletedAB
        res_body["byAutoManual"] = campaigns_email_send.byAutoManual

        sent_on = ""
        if campaigns_email_send.sendOnDate:
            sent_on = CommonFunction.convertEventTimeZoneToUser(
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

        # Variant A
        split_group = "A"
        link_count_total = 0
        ui = 0
        total_desktop = 0
        total_mobile = 0

        campaign_links_list = CampaignLinks.objects.filter(campId=dec_camp_id, splitGroup=split_group).order_by('id')
        for cll in campaign_links_list:
            link_count_total += cll.linkCount or 0
            pc = CampaignLinkClick.objects.filter(linkId=cll.id, sources='PC').count()
            total_desktop += pc
            phone = CampaignLinkClick.objects.filter(linkId=cll.id, sources='Phone').count()
            total_mobile += phone
            tc_count = CampaignLinkClick.objects.filter(linkId=cll.id).values('userId').distinct().count()
            ui += tc_count

        sent = CampaignsSendEmailArchive.objects.filter(campSendId=dec_camp_id, splitGroup=split_group).count()
        deliveries = CampaignsSendEmailArchive.objects.filter(campSendId=dec_camp_id, splitGroup=split_group, isSend='Y', isBounced='N').count()
        opened = CampaignsSendEmailArchive.objects.filter(campSendId=dec_camp_id, splitGroup=split_group, isRead='Y').count()
        bounced = CampaignsSendEmailArchive.objects.filter(campSendId=dec_camp_id, splitGroup=split_group, isBounced='Y').count()
        unsubscribed = CampaignsSendEmailArchive.objects.filter(campSendId=dec_camp_id, splitGroup=split_group, isUnsubscribed='Y').count()
        unread = deliveries - opened

        successful_deliveries = deliveries
        successful_deliveries_per = 0.0
        if sent > 0:
            successful_deliveries_per = (successful_deliveries / sent) * 100
        bounced_per = 0.0
        if sent > 0:
            bounced_per = (bounced * 100) / sent
        unsubscribed_per = 0.0
        if sent > 0:
            unsubscribed_per = (unsubscribed * 100) / sent
        open_rate_per = 0.0
        if deliveries > 0:
            open_rate_per = (opened * 100) / deliveries
        total_click_through_rate_per = 0.0
        if deliveries > 0:
            total_click_through_rate_per = (link_count_total * 100) / deliveries
        unique_click_through_rate_per = 0.0
        if successful_deliveries > 0:
            unique_click_through_rate_per = (ui * 100) / successful_deliveries

        dashboard["sentOn"] = sent_on
        dashboard["mailingGroup"] = group_name
        dashboard["subject"] = campaigns_email_send.subject
        dashboard["senderName"] = campaigns_email_send.fromName
        dashboard["senderEmail"] = campaigns_email_send.fromAdd
        dashboard["sent"] = sent
        dashboard["delivered"] = deliveries
        dashboard["opened"] = opened
        dashboard["bounced"] = bounced
        dashboard["unread"] = unread
        dashboard["totalDesktop"] = total_desktop
        dashboard["totalMobile"] = total_mobile
        dashboard["successfulDeliveries"] = successful_deliveries
        dashboard["successfulDeliveriesPer"] = successful_deliveries_per
        dashboard["bouncedPer"] = bounced_per
        dashboard["unsubscribed"] = unsubscribed
        dashboard["unsubscribedPer"] = unsubscribed_per
        dashboard["openRatePer"] = open_rate_per
        dashboard["totalClickThroughRate"] = link_count_total
        dashboard["totalClickThroughRatePer"] = total_click_through_rate_per
        dashboard["uniqueClickThroughRate"] = ui
        dashboard["uniqueClickThroughRatePer"] = unique_click_through_rate_per

        # Variant B
        split_group = "B"
        link_count_total_b = 0
        ui_b = 0
        total_desktop_b = 0
        total_mobile_b = 0

        campaign_links_list_b = CampaignLinks.objects.filter(campId=dec_camp_id, splitGroup=split_group).order_by('id')
        for cll in campaign_links_list_b:
            link_count_total_b += cll.linkCount or 0
            pc = CampaignLinkClick.objects.filter(linkId=cll.id, sources='PC').count()
            total_desktop_b += pc
            phone = CampaignLinkClick.objects.filter(linkId=cll.id, sources='Phone').count()
            total_mobile_b += phone
            tc_count = CampaignLinkClick.objects.filter(linkId=cll.id).values('userId').distinct().count()
            ui_b += tc_count

        sent_b = CampaignsSendEmailArchive.objects.filter(campSendId=dec_camp_id, splitGroup=split_group).count()
        deliveries_b = CampaignsSendEmailArchive.objects.filter(campSendId=dec_camp_id, splitGroup=split_group, isSend='Y', isBounced='N').count()
        opened_b = CampaignsSendEmailArchive.objects.filter(campSendId=dec_camp_id, splitGroup=split_group, isRead='Y').count()
        bounced_b = CampaignsSendEmailArchive.objects.filter(campSendId=dec_camp_id, splitGroup=split_group, isBounced='Y').count()
        unsubscribed_b = CampaignsSendEmailArchive.objects.filter(campSendId=dec_camp_id, splitGroup=split_group, isUnsubscribed='Y').count()
        unread_b = deliveries_b - opened_b

        successful_deliveries_b = deliveries_b
        successful_deliveries_per_b = 0.0
        if sent_b > 0:
            successful_deliveries_per_b = (successful_deliveries_b / sent_b) * 100
        bounced_per_b = 0.0
        if sent_b > 0:
            bounced_per_b = (bounced_b * 100) / sent_b
        unsubscribed_per_b = 0.0
        if sent_b > 0:
            unsubscribed_per_b = (unsubscribed_b * 100) / sent_b
        open_rate_per_b = 0.0
        if deliveries_b > 0:
            open_rate_per_b = (opened_b * 100) / deliveries_b
        total_click_through_rate_per_b = 0.0
        if deliveries_b > 0:
            total_click_through_rate_per_b = (link_count_total_b * 100) / deliveries_b
        unique_click_through_rate_per_b = 0.0
        if successful_deliveries_b > 0:
            unique_click_through_rate_per_b = (ui_b * 100) / successful_deliveries_b

        sent_on_b = ""
        if campaigns_email_send.sendOnDateB:
            sent_on_b = CommonFunction.convertEventTimeZoneToUser(
                CommonFunction.displayDateTime(str(campaigns_email_send.sendOnDateB)), "UTC", tempt_time_zone
            )

        dashboard_b["sentOn"] = sent_on_b
        dashboard_b["mailingGroup"] = group_name

        if campaigns_email_send.testingType in [2, 3, 6]:
            dashboard_b["subject"] = campaigns_email_send.subject
        else:
            dashboard_b["subject"] = campaigns_email_send.subjectB

        dashboard_b["senderName"] = campaigns_email_send.fromNameB
        dashboard_b["senderEmail"] = campaigns_email_send.fromAdd
        dashboard_b["sent"] = sent_b
        dashboard_b["delivered"] = deliveries_b
        dashboard_b["opened"] = opened_b
        dashboard_b["bounced"] = bounced_b
        dashboard_b["unread"] = unread_b
        dashboard_b["totalDesktop"] = total_desktop_b
        dashboard_b["totalMobile"] = total_mobile_b
        dashboard_b["successfulDeliveries"] = successful_deliveries_b
        dashboard_b["successfulDeliveriesPer"] = successful_deliveries_per_b
        dashboard_b["bouncedPer"] = bounced_per_b
        dashboard_b["unsubscribed"] = unsubscribed_b
        dashboard_b["unsubscribedPer"] = unsubscribed_per_b
        dashboard_b["openRatePer"] = open_rate_per_b
        dashboard_b["totalClickThroughRate"] = link_count_total_b
        dashboard_b["totalClickThroughRatePer"] = total_click_through_rate_per_b
        dashboard_b["uniqueClickThroughRate"] = ui_b
        dashboard_b["uniqueClickThroughRatePer"] = unique_click_through_rate_per_b

        # Winner Variant O
        split_group = "O"
        link_count_total_o = 0
        ui_o = 0
        total_desktop_o = 0
        total_mobile_o = 0

        campaign_links_list_o = CampaignLinks.objects.filter(campId=dec_camp_id, splitGroup=split_group).order_by('id')
        for cll in campaign_links_list_o:
            link_count_total_o += cll.linkCount or 0
            pc = CampaignLinkClick.objects.filter(linkId=cll.id, sources='PC').count()
            total_desktop_o += pc
            phone = CampaignLinkClick.objects.filter(linkId=cll.id, sources='Phone').count()
            total_mobile_o += phone
            tc_count = CampaignLinkClick.objects.filter(linkId=cll.id).values('userId').distinct().count()
            ui_o += tc_count

        sent_o = CampaignsSendEmailArchive.objects.filter(campSendId=dec_camp_id, splitGroup=split_group).count()
        deliveries_o = CampaignsSendEmailArchive.objects.filter(campSendId=dec_camp_id, splitGroup=split_group, isSend='Y', isBounced='N').count()
        opened_o = CampaignsSendEmailArchive.objects.filter(campSendId=dec_camp_id, splitGroup=split_group, isRead='Y').count()
        bounced_o = CampaignsSendEmailArchive.objects.filter(campSendId=dec_camp_id, splitGroup=split_group, isBounced='Y').count()
        unsubscribed_o = CampaignsSendEmailArchive.objects.filter(campSendId=dec_camp_id, splitGroup=split_group, isUnsubscribed='Y').count()
        unread_o = deliveries_o - opened_o

        successful_deliveries_o = deliveries_o
        successful_deliveries_per_o = 0.0
        if sent_o > 0:
            successful_deliveries_per_o = (successful_deliveries_o / sent_o) * 100
        bounced_per_o = 0.0
        if sent_o > 0:
            bounced_per_o = (bounced_o * 100) / sent_o
        unsubscribed_per_o = 0.0
        if sent_o > 0:
            unsubscribed_per_o = (unsubscribed_o * 100) / sent_o
        open_rate_per_o = 0.0
        if deliveries_o > 0:
            open_rate_per_o = (opened_o * 100) / deliveries_o
        total_click_through_rate_per_o = 0.0
        if deliveries_o > 0:
            total_click_through_rate_per_o = (link_count_total_o * 100) / deliveries_o
        unique_click_through_rate_per_o = 0.0
        if successful_deliveries_o > 0:
            unique_click_through_rate_per_o = (ui_o * 100) / successful_deliveries_o

        group_winner = CampaignsSendEmailArchive.objects.filter(campSendId=dec_camp_id, groupWinner__isnull=False).values_list('groupWinner', flat=True).distinct().first()
        if not group_winner:
            group_winner = ""

        subject_o = ""
        from_name_o = ""
        from_add_o = ""
        send_on_date_o = ""

        if group_winner == "A":
            subject_o = campaigns_email_send.subject
            from_name_o = campaigns_email_send.fromName
            from_add_o = campaigns_email_send.fromAdd
            send_on_date_o = sent_on
        elif group_winner == "B":
            subject_o = campaigns_email_send.subjectB
            from_name_o = campaigns_email_send.fromNameB
            from_add_o = campaigns_email_send.fromAdd
            send_on_date_o = sent_on_b

        dashboard_o["sentOn"] = send_on_date_o
        dashboard_o["mailingGroup"] = group_name
        dashboard_o["subject"] = subject_o
        dashboard_o["senderName"] = from_name_o
        dashboard_o["senderEmail"] = from_add_o
        dashboard_o["sent"] = sent_o
        dashboard_o["delivered"] = deliveries_o
        dashboard_o["opened"] = opened_o
        dashboard_o["bounced"] = bounced_o
        dashboard_o["unread"] = unread_o
        dashboard_o["totalDesktop"] = total_desktop_o
        dashboard_o["totalMobile"] = total_mobile_o
        dashboard_o["successfulDeliveries"] = successful_deliveries_o
        dashboard_o["successfulDeliveriesPer"] = successful_deliveries_per_o
        dashboard_o["bouncedPer"] = bounced_per_o
        dashboard_o["unsubscribed"] = unsubscribed_o
        dashboard_o["unsubscribedPer"] = unsubscribed_per_o
        dashboard_o["openRatePer"] = open_rate_per_o
        dashboard_o["totalClickThroughRate"] = link_count_total_o
        dashboard_o["totalClickThroughRatePer"] = total_click_through_rate_per_o
        dashboard_o["uniqueClickThroughRate"] = ui_o
        dashboard_o["uniqueClickThroughRatePer"] = unique_click_through_rate_per_o

        if group_winner == "A":
            winner = "A"
        elif group_winner == "B":
            winner = "B"

        last_opened = ""
        if campaigns_email_send.lastOpened:
            last_opened = CommonFunction.displayDateTime(str(campaigns_email_send.lastOpened))

        res_body["lastOpened"] = last_opened
        res_body["winner"] = winner
        res_body["dashboard"] = dashboard
        res_body["dashboardB"] = dashboard_b
        res_body["dashboardO"] = dashboard_o

        return CustomResponse(data=res_body, status=200, message="Email Campaigns Dashboard Fetched Successfully")
    except Exception as e:
        logger.error(f"[ memberId : {request.query_params.get('memberId')} ] GetEmailCampaignsReportDashboardAB Error : {e}", exc_info=True)
        return CustomResponse(data=res_body, status=500, message="error")


@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_email_campaigns_report_product_links_ab(request: Request) -> CustomResponse:
    res_body = {}
    try:
        camp_id_encrypted = request.query_params.get("campId")
        id_param = request.query_params.get("id")

        if not camp_id_encrypted:
            return CustomResponse(data=res_body, status=400, message="Missing campId")

        dec_camp_id = int(camp_id_encrypted)
        id_val = int(id_param) if id_param else 0

        res_body["productLinks"] = report_product_links(id_val, dec_camp_id, "A")
        res_body["productLinksB"] = report_product_links(id_val, dec_camp_id, "B")
        res_body["productLinksO"] = report_product_links(id_val, dec_camp_id, "O")

        return CustomResponse(data=res_body, status=200, message="Email Campaigns Product Links Fetched Successfully")
    except Exception as e:
        logger.error(f"[ campId : {request.query_params.get('campId')} ] GetEmailCampaignsReportProductLinksAB Error : {e}", exc_info=True)
        return CustomResponse(data=res_body, status=500, message="error")


@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_email_campaigns_report_members_list_page_ab(request: Request) -> CustomResponse:
    res_body = {}
    split_group = "A"
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
            member = Tenants.objects.select_related('details').filter(ten_id=get_client_id_by_tenant_id(int(member_id_param))).first()
            if member:
                final_member_id = CommonFunction.getFinalMemberId(member)

        if final_member_id is None and member_id_param:
            final_member_id = int(member_id_param)

        offset = page * size
        limit = offset + size

        queryset = CampaignsSendEmailArchive.objects.filter(campSendId=dec_camp_id, splitGroup=split_group).order_by('id')
        if search_key:
            queryset = queryset.filter(firstName__icontains=search_key)

        total_pages = math.ceil(queryset.count() / size) if size > 0 else 0
        paginated_members = queryset[offset:limit]

        total_campaigns_send_email = CampaignsSendEmailArchive.objects.filter(campSendId=dec_camp_id, splitGroup=split_group).count()

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
                campaign_links_list = CampaignLinks.objects.filter(campId=dec_camp_id, splitGroup=split_group).order_by('id')
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
        res_body["members"] = campaigns_send_email_dto_list

        return CustomResponse(data=res_body, status=200, message="Email Campaigns Member List Fetched Successfully")
    except Exception as e:
        logger.error(f"[ memberId : {request.query_params.get('memberId')} ] GetEmailCampaignsReportMembersAB Error : {e}", exc_info=True)
        return CustomResponse(data=res_body, status=500, message="error")


@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_email_campaigns_report_members_b_list_page_ab(request: Request) -> CustomResponse:
    res_body = {}
    split_group = "B"
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
            member = Tenants.objects.select_related("details").filter(ten_id=int(get_client_id_by_tenant_id(int(member_id_param)))).first()
            if member:
                final_member_id = CommonFunction.getFinalMemberId(member)

        if final_member_id is None and member_id_param:
            final_member_id = int(member_id_param)

        offset = page * size
        limit = offset + size

        queryset = CampaignsSendEmailArchive.objects.filter(campSendId=dec_camp_id, splitGroup=split_group).order_by('id')
        if search_key:
            queryset = queryset.filter(firstName__icontains=search_key)

        total_pages = math.ceil(queryset.count() / size) if size > 0 else 0
        paginated_members = queryset[offset:limit]

        total_campaigns_send_email = CampaignsSendEmailArchive.objects.filter(campSendId=dec_camp_id, splitGroup=split_group).count()

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
                campaign_links_list = CampaignLinks.objects.filter(campId=dec_camp_id, splitGroup=split_group).order_by('id')
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
        res_body["membersB"] = campaigns_send_email_dto_list

        return CustomResponse(data=res_body, status=200, message="Email Campaigns Member List B Fetched Successfully")
    except Exception as e:
        logger.error(f"[ memberId : {request.query_params.get('memberId')} ] GetEmailCampaignsReportMembersListBPageAB Error : {e}", exc_info=True)
        return CustomResponse(data=res_body, status=500, message="error")


@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_email_campaigns_report_members_o_list_page_ab(request: Request) -> CustomResponse:
    res_body = {}
    split_group = "O"
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
            member = Tenants.objects.select_related("details").filter(ten_id=int(get_client_id_by_tenant_id(int(member_id_param)))).first()
            if member:
                final_member_id = CommonFunction.getFinalMemberId(member)

        if final_member_id is None and member_id_param:
            final_member_id = int(member_id_param)

        offset = page * size
        limit = offset + size

        queryset = CampaignsSendEmailArchive.objects.filter(campSendId=dec_camp_id, splitGroup=split_group).order_by('id')
        if search_key:
            queryset = queryset.filter(firstName__icontains=search_key)

        total_pages = math.ceil(queryset.count() / size) if size > 0 else 0
        paginated_members = queryset[offset:limit]

        total_campaigns_send_email = CampaignsSendEmailArchive.objects.filter(campSendId=dec_camp_id, splitGroup=split_group).count()

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
                campaign_links_list = CampaignLinks.objects.filter(campId=dec_camp_id, splitGroup=split_group).order_by('id')
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
        res_body["membersO"] = campaigns_send_email_dto_list

        return CustomResponse(data=res_body, status=200, message="Email Campaigns Member List O Fetched Successfully")
    except Exception as e:
        logger.error(f"[ memberId : {request.query_params.get('memberId')} ] GetEmailCampaignsReportMembersOListPageAB Error : {e}", exc_info=True)
        return CustomResponse(data=res_body, status=500, message="error")


@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_email_campaigns_report_sources_ab(request: Request) -> CustomResponse:
    res_body = {}
    try:
        camp_id_encrypted = request.query_params.get("campId")
        id_param = request.query_params.get("id")

        if not camp_id_encrypted:
            return CustomResponse(data=res_body, status=400, message="Missing campId")

        dec_camp_id = int(camp_id_encrypted)
        id_val = int(id_param) if id_param else 0

        res_body["sourceLinks"] = report_sources(id_val, dec_camp_id, "A")
        res_body["sourceLinksB"] = report_sources(id_val, dec_camp_id, "B")
        res_body["sourceLinksO"] = report_sources(id_val, dec_camp_id, "O")

        return CustomResponse(data=res_body, status=200, message="Email Campaigns Product Sources Fetched Successfully")
    except Exception as e:
        logger.error(f"[ campId : {request.query_params.get('campId')} ] GetEmailCampaignsReportSourcesAB Error : {e}", exc_info=True)
        return CustomResponse(data=res_body, status=500, message="error")


@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_campaigns_report_print_ab(request: Request) -> CustomResponse:
    res_body = {}
    try:
        member_id_param = request.query_params.get("memberId")
        camp_id_encrypted = request.query_params.get("campId")
        id_param = request.query_params.get("id")

        if not member_id_param or not camp_id_encrypted:
            return CustomResponse(data=res_body, status=400, message="Missing required parameters")

        member_id = int(member_id_param)
        dec_camp_id = int(camp_id_encrypted)
        id_val = int(id_param) if id_param else 0

        member = Tenants.objects.select_related("details").filter(ten_id=int(get_client_id_by_tenant_id(int(member_id_param)))).first()
        final_member_id = CommonFunction.getFinalMemberId(member) if member else member_id

        res_body["productLinks"] = print_product_link(final_member_id, id_val, dec_camp_id, "A")
        res_body["productLinksB"] = print_product_link(final_member_id, id_val, dec_camp_id, "B")
        res_body["productLinksWinner"] = print_product_link(final_member_id, id_val, dec_camp_id, "O")

        res_body["members"] = print_members(final_member_id, id_val, dec_camp_id, "A")
        res_body["membersB"] = print_members(final_member_id, id_val, dec_camp_id, "B")
        res_body["membersWinner"] = print_members(final_member_id, id_val, dec_camp_id, "O")

        res_body["sourceLinks"] = print_sources(final_member_id, id_val, dec_camp_id, "A")
        res_body["sourceLinksB"] = print_sources(final_member_id, id_val, dec_camp_id, "B")
        res_body["sourceLinksWinner"] = print_sources(final_member_id, id_val, dec_camp_id, "O")

        return CustomResponse(data=res_body, status=200, message="Email Campaigns Report Print Fetched Successfully")
    except Exception as e:
        logger.error(f"[ memberId : {request.query_params.get('memberId')} ] GetCampaignsReportPrintAB Error : {e}", exc_info=True)
        return CustomResponse(data=res_body, status=500, message="error")


@api_view(['POST'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def set_choose_winner(request: Request) -> CustomResponse:
    res_body = {}
    try:
        camp_id_encrypted = request.data.get("campId")
        winner = request.data.get("winner")
        sub_member_id_param = request.data.get("subMemberId")

        if not camp_id_encrypted or not winner or sub_member_id_param is None:
            return CustomResponse(data=res_body, status=400, message="Missing required parameters")

        camp_id = int(camp_id_encrypted)
        sub_member_id = int(sub_member_id_param)

        smtp_servers = SmtpServer.objects.filter(isActive=1)
        server_domains = set()
        server_name = {}
        for s in smtp_servers:
            domain_str = s.serverDomain or ""
            domain_list = [d.strip() for d in domain_str.split(",") if d.strip()]
            server_domains.update(domain_list)
            server_name[s.serverName] = domain_list

        domain_in_server = {}
        domain_server_in_count = {}
        for d_value in server_domains:
            domain_server_in_count[d_value] = 0
            for key, temp_domains in server_name.items():
                if d_value in temp_domains:
                    if d_value in domain_in_server:
                        domain_in_server[d_value].append(key)
                    else:
                        domain_in_server[d_value] = [key]
                    domain_server_in_count[d_value] += 1

        if "others" in server_domains:
            server_domains.remove("others")

        campaigns_email_send = CampaignsEmailSend.objects.filter(id=camp_id).first()
        if not campaigns_email_send:
            return CustomResponse(data=res_body, status=404, message="Campaign not found")

        CampaignsEmail.objects.filter(campId=campaigns_email_send.campId).update(resultTie=None)
        CampaignsEmailSend.objects.filter(id=camp_id).update(resultTie=None)

        if winner == "A":
            split_group_param = "B"
            # insertCampaignsEmailSend
            records_to_copy = CampaignsSendEmail.objects.filter(
                campSendId=camp_id, splitGroup=split_group_param
            ).filter(
                django_models.Q(isBounced='N') | django_models.Q(isBounced__isnull=True)
            )
            to_create = []
            for r in records_to_copy:
                to_create.append(CampaignsSendEmail(
                    campId=r.campId,
                    campSendId=r.campSendId,
                    memberId=r.memberId,
                    emailId=r.emailId,
                    isSend='N',
                    isProcessed='N',
                    firstName=r.firstName,
                    lastName=r.lastName,
                    email=r.email,
                    emailDomain=r.emailDomain,
                    csDefaultLanguage=r.csDefaultLanguage,
                    splitGroup='O',
                    msgPriority=r.msgPriority,
                    subMemberId=sub_member_id
                ))
            CampaignsSendEmail.objects.bulk_create(to_create)

            # updateCampaignsEmailSendByCampSendId
            CampaignsSendEmail.objects.filter(campSendId=camp_id, splitGroup='O').update(groupWinner='A', subMemberId=sub_member_id)

            # getMemberListCount
            member_list = CampaignsSendEmail.objects.filter(groupWinner='A', subMemberId=sub_member_id, campSendId=camp_id, splitGroup='O').count()

            member = Tenants.objects.select_related('details').filter(ten_id=get_client_id_by_tenant_id(campaigns_email_send.memberId)).first()
            country_setting = country_setting_by_member_id(member.ten_id) if member else None
            total_amount = CommonFunction.campaignPriceListDisplay(member_list, country_setting) if country_setting else 0.0
            member_rate = CommonFunction.campaignPriceListPer(member_list, country_setting) if country_setting else 0.0

            save_campaign_transaction(
                tran_campaign_id=int(campaigns_email_send.campId),
                tran_campaign_name=f"{campaigns_email_send.campName}-send winner campaign",
                tran_total_member=member_list,
                tran_type="campaign",
                tran_invoiced_id=None,
                tran_invoiced_status="uninvoiced",
                tran_invoiced_date=None,
                member_id=campaigns_email_send.memberId,
                tran_bill_type="0",
                tran_total_amount=total_amount,
                tran_member_rate=member_rate,
                tran_count_total_sms=0,
                tran_poll_form_no=None,
                tran_poll_to_no=None,
                sub_member_id=sub_member_id
            )
            res_body["msg"] = "A Campaign Is Send To Remain Contacts."

        elif winner == "B":
            split_group_param = "A"
            # insertCampaignsEmailSend
            records_to_copy = CampaignsSendEmail.objects.filter(
                campSendId=camp_id, splitGroup=split_group_param
            ).filter(
                django_models.Q(isBounced='N') | django_models.Q(isBounced__isnull=True)
            )
            to_create = []
            for r in records_to_copy:
                to_create.append(CampaignsSendEmail(
                    campId=r.campId,
                    campSendId=r.campSendId,
                    memberId=r.memberId,
                    emailId=r.emailId,
                    isSend='N',
                    isProcessed='N',
                    firstName=r.firstName,
                    lastName=r.lastName,
                    email=r.email,
                    emailDomain=r.emailDomain,
                    csDefaultLanguage=r.csDefaultLanguage,
                    splitGroup='O',
                    msgPriority=r.msgPriority,
                    subMemberId=sub_member_id
                ))
            CampaignsSendEmail.objects.bulk_create(to_create)

            # updateCampaignsEmailSendByCampSendId
            CampaignsSendEmail.objects.filter(campSendId=camp_id, splitGroup='O').update(groupWinner='B', subMemberId=sub_member_id)

            # getMemberListCount
            member_list = CampaignsSendEmail.objects.filter(groupWinner='B', subMemberId=sub_member_id, campSendId=camp_id, splitGroup='O').count()

            member = Tenants.objects.select_related('details').filter(ten_id=get_client_id_by_tenant_id(campaigns_email_send.memberId)).first()
            country_setting = country_setting_by_member_id(member.ten_id) if member else None
            total_amount = CommonFunction.campaignPriceListDisplay(member_list, country_setting) if country_setting else 0.0
            member_rate = CommonFunction.campaignPriceListPer(member_list, country_setting) if country_setting else 0.0

            save_campaign_transaction(
                tran_campaign_id=int(campaigns_email_send.campId),
                tran_campaign_name=f"{campaigns_email_send.campName}-send winner campaign",
                tran_total_member=member_list,
                tran_type="campaign",
                tran_invoiced_id=None,
                tran_invoiced_status="uninvoiced",
                tran_invoiced_date=None,
                member_id=campaigns_email_send.memberId,
                tran_bill_type="0",
                tran_total_amount=total_amount,
                tran_member_rate=member_rate,
                tran_count_total_sms=0,
                tran_poll_form_no=None,
                tran_poll_to_no=None,
                sub_member_id=sub_member_id
            )
            res_body["msg"] = "B Campaign Is Send To Remain Contacts."

        # domain redistribution
        # getDomainValueTotal
        d_value_total = CampaignsSendEmailArchive.objects.filter(campSendId=camp_id).exclude(emailDomain__in=list(server_domains)).count()
        others_count = domain_server_in_count.get("others", 0)
        if others_count > 0:
            d_value_limit = int(math.ceil(d_value_total / float(others_count)))
            st_point = 0
            for ds_value in domain_in_server.get("others", []):
                ids = list(CampaignsSendEmail.objects.filter(campSendId=camp_id).exclude(emailDomain__in=list(server_domains)).order_by('id').values_list('id', flat=True)[st_point : st_point + d_value_limit])
                if ids:
                    CampaignsSendEmailArchive.objects.filter(id__in=ids).update(smtpServerHost=ds_value, subMemberId=sub_member_id)
                st_point += d_value_limit

        if "others" in domain_server_in_count:
            del domain_server_in_count["others"]
        if "others" in domain_in_server:
            del domain_in_server["others"]

        for d_value in server_domains:
            # getDomainValueTotalByEmailDomain
            d_value_total_1 = CampaignsSendEmailArchive.objects.filter(campSendId=camp_id, emailDomain=d_value).count()
            srv_count = domain_server_in_count.get(d_value, 0)
            if srv_count > 0:
                d_value_limit_1 = int(math.ceil(d_value_total_1 / float(srv_count)))
                st_point_1 = 0
                for ds_value in domain_in_server.get(d_value, []):
                    ids = list(CampaignsSendEmail.objects.filter(campSendId=camp_id, emailDomain=d_value).order_by('id').values_list('id', flat=True)[st_point_1 : st_point_1 + d_value_limit_1])
                    if ids:
                        CampaignsSendEmailArchive.objects.filter(id__in=ids).update(smtpServerHost=ds_value, subMemberId=sub_member_id)
                    st_point_1 += d_value_limit_1

        return CustomResponse(data=res_body, status=200, message="Winner Set Successfully")
    except Exception as e:
        logger.error(f"[ campId : {request.data.get('campId')} ] SetChooseWinner Error : {e}", exc_info=True)
        return CustomResponse(data=res_body, status=500, message="error")


@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_email_campaigns_report_members_list_ab(request: Request) -> CustomResponse:
    res_body = {}
    campaigns_send_email_dto_list = []
    res_body["members"] = campaigns_send_email_dto_list
    try:
        member_id_param = request.query_params.get("memberId")
        camp_id_encrypted = request.query_params.get("campId")
        split_group = request.query_params.get("splitGroup", "")

        if not member_id_param or not camp_id_encrypted or not split_group:
            return CustomResponse(data=res_body, status=400, message="Missing required parameters")

        member_id = int(member_id_param)
        dec_camp_id = int(camp_id_encrypted)

        member = Tenants.objects.select_related('details').filter(ten_id=get_client_id_by_tenant_id(member_id)).first()
        final_member_id = CommonFunction.getFinalMemberId(member) if member else member_id

        camp_name_val = CampaignsEmailSend.objects.filter(id=dec_camp_id).values_list('campName', flat=True).first()
        res_body["campName"] = camp_name_val or ""

        campaigns_email_send_list = CampaignsSendEmailArchive.objects.filter(campSendId=dec_camp_id, splitGroup=split_group).order_by('firstName')
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
