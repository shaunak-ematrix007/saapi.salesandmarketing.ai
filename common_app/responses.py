from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional
from rest_framework.response import Response

class CustomResponse(Response):
    """
    Custom Django REST Framework Response matching the Spring Boot ApiResponse and ResponseObject format.
    Ensures consistent serialization structures across both frameworks.

    Output format:
    {
        "status": <HTTP Status Code (int)>,
        "message": "<Status/Error Message (str)>",
        "result": <Payload Data (Any)>
    }
    """
    def __init__(
        self,
        data: Optional[Any] = None,
        status: int = 200,
        message: str = "Success",
        headers: Optional[Dict[str, str]] = None,
        exception: bool = False,
        content_type: Optional[str] = None
    ) -> None:
        payload: Dict[str, Any] = {
            "status": status,
            "message": message,
            "result": data
        }
        super().__init__(
            data=payload,
            status=status,
            headers=headers,
            exception=exception,
            content_type=content_type
        )


@dataclass
class AuthorizedUser:
    """
    Standard Python dataclass representing AuthorizedUser session data.
    Translated from Java's AuthorizedUser.java and fully typed.
    """
    memberId: Optional[int]
    username: str
    firstName: Optional[str]
    lastName: Optional[str]
    password: Optional[str] = None
    authorities: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """
        Serializes AuthorizedUser session data to a standard Python dictionary.
        """
        return asdict(self)
