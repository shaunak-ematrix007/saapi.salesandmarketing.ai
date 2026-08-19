from common_app.utils import get_client_id_by_tenant_id
import logging
import math
from typing import Any, Dict
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated

from auth_app.authentication import CustomJWTAuthentication
from common_app.models import (
    SmtpServer, CampaignsEmailSend, CampaignsEmail, Tenants, Clients,
    CampaignsSendEmail, CampaignsSendEmailArchive, AutomationSendContact
)
from common_app.responses import CustomResponse
from common_app.common_function import CommonFunction
from common_app.utils import *

logger = logging.getLogger(__name__)


def check_camp_status(camp_status: int, total_members: int, camp_id: int, camp_send_id: int) -> str:
    """Helper to determine the campaign status string matching Java logic."""
    status_str = ""
    if camp_status in [0, 1]:
        status_str = "Draft"
    elif camp_status == 2:
        total_delivered = CampaignsSendEmail.objects.filter(
            campId=camp_id,
            campSendId=camp_send_id,
            isSend='Y'
        ).count()
        if total_members > 0 and (total_delivered / total_members == 1):
            status_str = "Completed"
    elif camp_status == 3:
        status_str = "Completed"
    elif camp_status == 4:
        status_str = "Delete Pending"
    return status_str


def check_camp_status_archive(camp_status: int, total_members: int, camp_id: int, camp_send_id: int) -> str:
    """Helper to determine the archived campaign status string matching Java logic."""
    status_str = ""
    if camp_status in [0, 1]:
        status_str = "Draft"
    elif camp_status == 2:
        total_delivered = CampaignsSendEmailArchive.objects.filter(
            campId=camp_id,
            campSendId=camp_send_id,
            isSend='Y'
        ).count()
        if total_members > 0 and (total_delivered / total_members == 1):
            status_str = "Completed"
    elif camp_status == 3:
        status_str = "Completed"
    elif camp_status == 4:
        status_str = "Delete Pending"
    return status_str


@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_campaign_wise_email_campaign_list(request: Request) -> CustomResponse:
    """
    Returns a paginated list of campaign-wise email campaigns.
    Translates logic from EmailCampaignServiceImpl.getCampaignWiseEmailCampaignList.
    """
    res_body: Dict[str, Any] = {}
    try:
        search_key = request.query_params.get("searchKey", "")
        page = int(request.query_params.get("page", 0))
        size = int(request.query_params.get("size", 10))

        offset = page * size
        limit = offset + size

        queryset = CampaignsEmailSend.objects.all().order_by('id')

        if search_key:
            queryset = queryset.filter(campName__icontains=search_key)

        total_records = CampaignsEmailSend.objects.count()
        filtered_count = queryset.count()
        total_pages = math.ceil(filtered_count / size) if size > 0 else 0

        paginated_campaigns = queryset[offset:limit]

        email_campaign_dtos = []
        for campaigns_email in paginated_campaigns:
            try:
                camp_id = campaigns_email.campId
                camp_send_id = campaigns_email.id

                # Retrieve Member and decrypt details
                member = Tenants.objects.select_related('details').filter(ten_id=get_client_id_by_tenant_id(campaigns_email.memberId)).first()
                member_name = None
                company_name = None
                if member:
                    first_dec = member.ten_first_name or ""
                    last_dec = member.ten_last_name or ""
                    member_name = f"{first_dec} {last_dec}".strip()
                    company_name = get_company_name(campaigns_email.memberId)

                # Count sent/delivered stats
                total_members = CampaignsSendEmail.objects.filter(campId=camp_id, campSendId=camp_send_id).count()

                # Pending count queries
                pending_members = CampaignsSendEmail.objects.filter(
                    campId=camp_id,
                    campSendId=camp_send_id,
                    isSend='N'
                ).count()

                # Pay special attention to the logic used for counting queued campaign emails on tbl_automation_send_contact
                automation_queued = AutomationSendContact.objects.filter(campaignId=camp_id, status='QUEUED').count()
                pending_members += automation_queued

                # Camp status
                camp_status_val = CampaignsEmail.objects.filter(campId=camp_id).values_list('campStatus', flat=True).first()
                camp_status = camp_status_val if camp_status_val is not None else 0

                status = check_camp_status(camp_status, total_members, camp_id, camp_send_id)

                email_campaign_dtos.append({
                    "campSendId": camp_send_id,
                    "memberId": get_client_id_by_tenant_id(campaigns_email.memberId),
                    "memberName": member_name,
                    "companyName": company_name,
                    "campaignName": campaigns_email.campName,
                    "totalMembers": total_members,
                    "pendingMembers": pending_members,
                    "campStatus": camp_status,
                    "status": status
                })
            except Exception as item_err:
                logger.error(f"Error mapping campaignsEmail ID {campaigns_email.id}: {item_err}", exc_info=True)

        res_body["getTotalPages"] = total_pages
        res_body["getNumber"] = page
        res_body["getSize"] = size
        res_body["getTotalRecords"] = total_records
        res_body["emailCampaignsList"] = email_campaign_dtos

        return CustomResponse(data=res_body, status=200, message="Email Campaigns List Successfully Fetched")
    except Exception as e:
        logger.error(f"get_campaign_wise_email_campaign_list error: {e}", exc_info=True)
        return CustomResponse(data=res_body, status=500, message="Failed to fetch Email Campaigns List")


@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_server_wise_email_campaign_list(request: Request) -> CustomResponse:
    """
    Returns a paginated list of SMTP servers and their queued campaign statistics.
    Translates logic from EmailCampaignServiceImpl.getServerWiseEmailCampaignsList.
    """
    res_body: Dict[str, Any] = {}
    try:
        search_key = request.query_params.get("searchKey", "")
        page = int(request.query_params.get("page", 0))
        size = int(request.query_params.get("size", 10))

        offset = page * size
        limit = offset + size

        queryset = SmtpServer.objects.all().order_by('serverId')

        if search_key:
            queryset = queryset.filter(serverName__icontains=search_key)

        total_records = SmtpServer.objects.count()
        filtered_count = queryset.count()
        total_pages = math.ceil(filtered_count / size) if size > 0 else 0

        paginated_servers = queryset[offset:limit]

        server_wise_dtos = []
        for smtp_server in paginated_servers:
            # count server wise email campaigns
            total_queued = CampaignsSendEmail.objects.filter(
                smtpServerHost=smtp_server.serverDomain
            ).exclude(isSend='Y').exclude(isProcessed='Y').count()

            status = "Active" if smtp_server.isActive == 1 else "Inactive"

            server_wise_dtos.append({
                "serverName": smtp_server.serverName,
                "serverDomain": smtp_server.serverDomain,
                "countryName": smtp_server.country,
                "totalQueued": total_queued,
                "status": status
            })

        res_body["getTotalPages"] = total_pages
        res_body["getNumber"] = page
        res_body["getSize"] = size
        res_body["getTotalRecords"] = total_records
        res_body["serverWiseEmailCampaignsList"] = server_wise_dtos

        return CustomResponse(data=res_body, status=200, message="Server wise Email Campaigns List Successfully Fetched")
    except Exception as e:
        logger.error(f"get_server_wise_email_campaign_list error: {e}", exc_info=True)
        return CustomResponse(data=res_body, status=500, message="Failed to fetch server wise Email Campaigns List")


@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_contact_list_by_camp_id(request: Request) -> CustomResponse:
    """
    Returns contact list by campaign send ID and status (completed, pending, bad).
    Translates logic from EmailCampaignServiceImpl.getContactListByCampId.
    """
    res_body: Dict[str, Any] = {}
    try:
        search_key = request.query_params.get("searchKey", "")
        email_status = request.query_params.get("emailStatus", "").lower()
        camp_send_id = int(request.query_params.get("campSendId", 0))

        page = int(request.query_params.get("page", 0))
        size = int(request.query_params.get("size", 10))

        offset = page * size
        limit = offset + size

        queryset = CampaignsSendEmail.objects.filter(campSendId=camp_send_id).order_by('id')

        if email_status == "completed":
            queryset = queryset.filter(isSend='Y', isProcessed='Y')
        elif email_status == "pending":
            queryset = queryset.filter(isSend='N')
        elif email_status == "bad":
            queryset = queryset.filter(isBounced='N')

        if search_key:
            queryset = queryset.filter(firstName__icontains=search_key)

        filtered_count = queryset.count()
        total_pages = math.ceil(filtered_count / size) if size > 0 else 0

        paginated_contacts = queryset[offset:limit]

        contact_dtos = []
        for campaign_send_email in paginated_contacts:
            email_dec = campaign_send_email.email
            contact_dtos.append({
                "firstName": campaign_send_email.firstName,
                "lastName": campaign_send_email.lastName,
                "domain": campaign_send_email.emailDomain,
                "email": email_dec,
                "serverName": campaign_send_email.smtpServerHost
            })

        res_body["getTotalPages"] = total_pages
        res_body["getNumber"] = page
        res_body["getSize"] = size
        res_body["getTotalRecords"] = filtered_count
        res_body["getContactListByCampId"] = contact_dtos

        return CustomResponse(data=res_body, status=200, message="Contact List By CampId Successfully Fetched")
    except Exception as e:
        logger.error(f"get_contact_list_by_camp_id error: {e}", exc_info=True)
        return CustomResponse(data=res_body, status=500, message="Failed to fetch ContactListByCampId")


@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_server_list_by_camp_id(request: Request, campSendId: int) -> CustomResponse:
    """
    Returns SMTP server list configuration for a campaign send ID.
    Translates logic from EmailCampaignServiceImpl.getServerListByCampId.
    """
    res_body: Dict[str, Any] = {}
    try:
        # Get unique server domains
        server_hosts = CampaignsSendEmail.objects.filter(
            campSendId=campSendId
        ).values_list('smtpServerHost', flat=True).distinct()

        smtp_server_dtos = []
        for host in server_hosts:
            if not host:
                continue
            is_active_val = SmtpServer.objects.filter(serverDomain=host).values_list('isActive', flat=True).first()
            smtp_server_dtos.append({
                "serverName": host,
                "isActive": is_active_val if is_active_val is not None else 0
            })

        res_body["serversList"] = smtp_server_dtos
        return CustomResponse(data=res_body, status=200, message="Servers List By CampId Successfully Fetched")
    except Exception as e:
        logger.error(f"get_server_list_by_camp_id error: {e}", exc_info=True)
        return CustomResponse(data=res_body, status=500, message="Failed to fetch Servers List By CampId")


@api_view(['POST'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def reassign_server(request: Request) -> CustomResponse:
    """
    Partitions pending campaigns sends to a new list of target SMTP servers.
    Translates logic from EmailCampaignServiceImpl.reAssignServer.
    """
    try:
        re_assign_server_dto = request.data
        camp_send_id = re_assign_server_dto.get("campSendId")
        server_name_list = re_assign_server_dto.get("serverNameList", [])

        num_parts = len(server_name_list)
        if num_parts > 0:
            campaigns_send_emails = list(CampaignsSendEmail.objects.filter(
                campSendId=camp_send_id,
                isSend='N'
            ))
            total_elements = len(campaigns_send_emails)

            if total_elements > 0:
                if total_elements < num_parts:
                    for i in range(total_elements):
                        campaigns_send_emails[i].smtpServerHost = server_name_list[i]
                        campaigns_send_emails[i].save()
                else:
                    part_size = total_elements // num_parts
                    remaining_elements = total_elements % num_parts

                    part_sizes = []
                    for i in range(num_parts):
                        current_part_size = part_size + (1 if i < remaining_elements else 0)
                        part_sizes.add(current_part_size) if hasattr(part_sizes, 'add') else part_sizes.append(current_part_size)

                    start_idx = 0
                    for s_idx, size in enumerate(part_sizes):
                        server_name = server_name_list[s_idx]
                        for idx in range(start_idx, start_idx + size):
                            campaigns_send_emails[idx].smtpServerHost = server_name
                            campaigns_send_emails[idx].save()
                        start_idx += size
            else:
                logger.warning("no pending records for reassignment")
        else:
            logger.error("Server names required for reassignment")

        return CustomResponse(data=None, status=200, message="Reassginment of server Successfully done")
    except Exception as e:
        logger.error(f"reassign_server error: {e}", exc_info=True)
        return CustomResponse(data=None, status=500, message="Failed to re assgin server")


@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_archive_email_campaign_list(request: Request) -> CustomResponse:
    """
    Returns a paginated list of archived email campaigns.
    Translates logic from EmailCampaignServiceImpl.getArchiveEmailCampaignList.
    """
    res_body: Dict[str, Any] = {}
    try:
        member_id = int(request.query_params.get("memberId", 0))
        search_key = request.query_params.get("searchKey", "")
        page = int(request.query_params.get("page", 0))
        size = int(request.query_params.get("size", 10))

        offset = page * size
        limit = offset + size

        # Fetch member details
        member = Tenants.objects.select_related('details').filter(ten_id=get_client_id_by_tenant_id(member_id)).first()
        res_body["firstName"] = member.ten_first_name if member else None
        res_body["lastName"] = member.ten_last_name if member else None

        queryset = CampaignsEmail.objects.filter(memberId=get_client_id_by_tenant_id(member_id), archiveYn='Y').order_by('campId')

        if search_key:
            queryset = queryset.filter(campName__icontains=search_key)

        filtered_count = queryset.count()
        total_pages = math.ceil(filtered_count / size) if size > 0 else 0

        paginated_campaigns = queryset[offset:limit]

        email_campaign_dtos = []
        for campaigns_email in paginated_campaigns:
            try:
                send_date_str = ""
                if campaigns_email.sendDate:
                    send_date_str = CommonFunction.displayDateTime(str(campaigns_email.sendDate))

                send_on_date_str = ""
                if campaigns_email.sendOnDate:
                    send_on_date_str = CommonFunction.displayDateTime(str(campaigns_email.sendOnDate))

                email_campaign_dtos.append({
                    "campId": campaigns_email.campId,
                    "campName": campaigns_email.campName,
                    "sendDate": send_date_str,
                    "sendOnDate": send_on_date_str
                })
            except Exception as item_err:
                logger.error(f"Error mapping archived campaign {campaigns_email.campId}: {item_err}", exc_info=True)

        res_body["getTotalPages"] = total_pages
        res_body["getNumber"] = page
        res_body["getSize"] = size
        res_body["emailCampaignsList"] = email_campaign_dtos

        total_campaign = CampaignsEmail.objects.filter(memberId=get_client_id_by_tenant_id(member_id), archiveYn='Y').count()
        res_body["totalCampaign"] = total_campaign

        return CustomResponse(data=res_body, status=200, message="Email Campaigns List Successfully Fetched")
    except Exception as e:
        logger.error(f"get_archive_email_campaign_list error: {e}", exc_info=True)
        return CustomResponse(data=res_body, status=500, message="Failed to fetch Email Campaigns List")
