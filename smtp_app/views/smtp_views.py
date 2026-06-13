from typing import Any, Dict, Optional
import logging

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated

from auth_app.authentication import CustomJWTAuthentication
from common_app.models import SmtpServer
from common_app.responses import CustomResponse

logger = logging.getLogger(__name__)


def serialize_smtp_server_dto(smtp: Optional[SmtpServer]) -> Dict[str, Any]:
    """
    Serializes a SmtpServer instance to the exact camelCase SmtpServerDto structure.
    """
    if not smtp:
        return {}
    return {
        "serverId": smtp.serverId,
        "serverName": smtp.serverName,
        "serverDomain": smtp.serverDomain,
        "location": smtp.location,
        "country": smtp.country,
        "threads": smtp.threads,
        "mps": float(smtp.mps) if smtp.mps is not None else None,
        "pctFailure": float(smtp.pctFailure) if smtp.pctFailure is not None else None,
        "isActive": smtp.isActive
    }


def deserialize_smtp_server_dto_to_entity(data: Dict[str, Any], smtp: SmtpServer) -> SmtpServer:
    """
    Maps fields from the incoming payload (SmtpServerDto representation) to a SmtpServer instance.
    """
    smtp.serverName = data.get("serverName")
    smtp.serverDomain = data.get("serverDomain")
    smtp.location = data.get("location")
    smtp.country = data.get("country")

    threads = data.get("threads")
    smtp.threads = int(threads) if threads is not None else None

    mps = data.get("mps")
    smtp.mps = float(mps) if mps is not None else None

    pct_failure = data.get("pctFailure")
    smtp.pctFailure = float(pct_failure) if pct_failure is not None else None

    is_active = data.get("isActive")
    smtp.isActive = int(is_active) if is_active is not None else 1

    return smtp


@api_view(['POST'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def save_smtp_server(request: Request) -> CustomResponse:
    """
    POST /smtpServer/saveSmtpServer
    Saves or updates an SMTP Server relayer.
    """
    res_body: Dict[str, Any] = {}
    try:
        data: Dict[str, Any] = request.data
        server_id: Optional[int] = data.get("serverId")

        smtp_server = None
        if server_id is not None:
            try:
                smtp_server = SmtpServer.objects.get(serverId=server_id)
            except SmtpServer.DoesNotExist:
                pass

        if smtp_server is None:
            smtp_server = SmtpServer()

        deserialize_smtp_server_dto_to_entity(data, smtp_server)
        smtp_server.save()

        res_body["smtpServer"] = serialize_smtp_server_dto(smtp_server)
        return CustomResponse(data=res_body, status=200, message="Email Relayer saved successfully")
    except Exception as ex:
        logger.error(f"saveSmtpServer error : {str(ex)}")
        return CustomResponse(data=res_body, status=500, message="Email Relayer Save Fail")


@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_smtp_server(request: Request, smtpId: int) -> CustomResponse:
    """
    GET /smtpServer/getSmtpServer/{smtpId}
    Fetches details of a specific SMTP Server relayer.
    """
    res_body: Dict[str, Any] = {}
    try:
        try:
            smtp_server = SmtpServer.objects.get(serverId=smtpId)
            res_body["smtpServer"] = serialize_smtp_server_dto(smtp_server)
        except SmtpServer.DoesNotExist:
            pass
        return CustomResponse(data=res_body, status=200, message="Email Relayer fetched successfully")
    except Exception as ex:
        logger.error(f"getSmtpServer error : {str(ex)}")
        return CustomResponse(data=res_body, status=500, message="Email Relayer Fetch Fail")


@api_view(['DELETE'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_smtp_server(request: Request, smtpId: int) -> CustomResponse:
    """
    DELETE /smtpServer/deleteSmtpServer/{smtpId}
    Deletes an SMTP Server relayer by ID.
    """
    res_body: Dict[str, Any] = {}
    try:
        try:
            smtp_server = SmtpServer.objects.get(serverId=smtpId)
            smtp_server.delete()
        except SmtpServer.DoesNotExist:
            pass
        return CustomResponse(data=res_body, status=200, message="Email Relayer Deleted Successfully")
    except Exception as ex:
        logger.error(f"smtpServer delete error : {str(ex)}")
        return CustomResponse(data=res_body, status=500, message="Email Relayer Deleted Fail")


@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_all_smtp_servers(request: Request) -> CustomResponse:
    """
    GET /smtpServer/getAllSmtpServers
    Fetches paginated list of SMTP Server relayers.
    """
    res_body: Dict[str, Any] = {}
    try:
        try:
            page_num = int(request.query_params.get("page", 0))
            if page_num < 0:
                page_num = 0
        except (TypeError, ValueError):
            page_num = 0

        try:
            size = int(request.query_params.get("size", 10))
            if size <= 0:
                size = 10
        except (TypeError, ValueError):
            size = 10

        queryset = SmtpServer.objects.all().order_by("serverId")
        total_records = queryset.count()

        total_pages = (total_records + size - 1) // size if total_records > 0 else 0
        offset = page_num * size
        sliced_qs = queryset[offset:offset + size]

        smtp_server_dtos = [serialize_smtp_server_dto(s) for s in sliced_qs]

        res_body["getTotalPages"] = total_pages
        res_body["getNumber"] = page_num
        res_body["getSize"] = size
        res_body["subaccountPageList"] = smtp_server_dtos
        res_body["getTotalRecords"] = total_records

        return CustomResponse(data=res_body, status=200, message="Email Relayers list fetched successfully")
    except Exception as ex:
        logger.error(f"SmtpServers list error : {str(ex)}")
        return CustomResponse(data=res_body, status=500, message="Email Relayers  List failed to Fetch")
