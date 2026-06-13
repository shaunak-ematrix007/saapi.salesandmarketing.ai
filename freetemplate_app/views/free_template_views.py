from typing import Any, Dict, Optional
import logging

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated

from auth_app.authentication import CustomJWTAuthentication
from common_app.models import FreeTemplate
from common_app.responses import CustomResponse

logger = logging.getLogger(__name__)


def serialize_free_template_dto(ft: Optional[FreeTemplate]) -> Dict[str, Any]:
    """
    Serializes a FreeTemplate model instance to a camelCase dictionary representation.
    """
    if not ft:
        return {}

    folder_name: str = ft.ftFolderName or ""
    # Strip any slashes as done in FreeTemplateServiceImpl.java:
    folder_name = folder_name.replace("/", "")

    return {
        "ftId": ft.ftId,
        "ftName": ft.ftName,
        "ftFolderName": folder_name,
        "ftTags": ft.ftTags
    }


@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_free_template_list(request: Request, mpStageId: int) -> CustomResponse:
    """
    GET /freeTemplate/getFreeTemplateList/{mpStageId}
    Fetches the list of free templates filtered by stage ID, ordered by template name.
    """
    res_body: Dict[str, Any] = {}
    try:
        free_templates = FreeTemplate.objects.filter(ftStage=mpStageId).order_by('ftName')
        dtos = [serialize_free_template_dto(ft) for ft in free_templates]
        res_body["freeTemplate"] = dtos
        return CustomResponse(data=res_body, status=200, message="Free template fetched successfully.")
    except Exception as ex:
        logger.error(f"FindAllFreeTemplate Error : {str(ex)}")
        return CustomResponse(data=res_body, status=500, message="error")
