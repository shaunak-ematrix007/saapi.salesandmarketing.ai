import bcrypt
from typing import Any, Dict, List, Optional
from django.utils import timezone
from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.request import Request
from rest_framework.permissions import AllowAny, IsAuthenticated
from auth_app.authentication import CustomJWTAuthentication
from common_app.models import Admin, AdminPage, AdminPageDetails
from common_app.responses import CustomResponse
from auth_app.utils import generate_admin_token

def serialize_admin_dto(admin: Optional[Admin], include_password: bool = False) -> Dict[str, Any]:
    """
    Translates an Admin model instance into the exact camelCase AdminDto representation.
    """
    if not admin:
        return {}
    res = {
        "memberId": admin.memberId,
        "userName": admin.userName,
        "firstName": admin.firstName,
        "lastName": admin.lastName,
        "email": admin.email,
        "active": admin.active,
        "dateRegistered": admin.dateRegistered.strftime("%m/%d/%Y") if admin.dateRegistered else None,
        "lastLoggedIn": admin.lastLoggedIn.strftime("%m/%d/%Y") if admin.lastLoggedIn else None,
        "userType": admin.userType
    }
    if include_password:
        res["password"] = admin.password
    return res


@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_admin_by_id(request: Request, adminId: int) -> CustomResponse:
    """
    Fetches an admin user by ID and returns its AdminDto representation.
    """
    res_body: Dict[str, Any] = {}
    try:
        admin = Admin.objects.get(memberId=adminId)
        res_body["adminById"] = serialize_admin_dto(admin)
    except Admin.DoesNotExist:
        return CustomResponse(data=res_body, status=500, message="User fetched fail")
    except Exception:
        return CustomResponse(data=res_body, status=500, message="User fetched fail")
    return CustomResponse(data=res_body, status=200, message="User fetched successfully")


@api_view(['DELETE'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_admin(request: Request) -> CustomResponse:
    """
    Deletes specified admin users by their member IDs.
    """
    res_body: Dict[str, Any] = {}
    try:
        member_ids: List[int] = request.data.get("memberIds", [])
        for m_id in member_ids:
            Admin.objects.filter(memberId=m_id).delete()
    except Exception:
        return CustomResponse(data=res_body, status=500, message="Error in deleting users.")
    return CustomResponse(data=res_body, status=200, message="Users deleted successfully.")


@api_view(['POST'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def save_admin(request: Request) -> CustomResponse:
    """
    Creates a new admin user or updates an existing one. Hashes password securely via BCrypt.
    """
    res_body: Dict[str, Any] = {}
    try:
        data: Dict[str, Any] = request.data
        member_id: Optional[int] = data.get("memberId")
        
        if member_id and member_id > 0:
            try:
                admin = Admin.objects.get(memberId=member_id)
                message = "Admin updated successfully"
            except Admin.DoesNotExist:
                admin = Admin()
                admin.dateRegistered = timezone.now()
                message = "Admin saved successfully"
        else:
            admin = Admin()
            admin.dateRegistered = timezone.now()
            message = "Admin saved successfully"
            
        admin.userName = data.get("userName")
        
        password: Optional[str] = data.get("password")
        if password:
            hashed_bytes = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            admin.password = hashed_bytes.decode('utf-8')
        elif not member_id:
            admin.password = ""
            
        admin.firstName = data.get("firstName")
        admin.lastName = data.get("lastName")
        admin.email = data.get("email")
        admin.active = data.get("active", "Y")
        admin.userType = data.get("userType", 1)
        
        admin.save()
        res_body["msg"] = message
    except Exception:
        return CustomResponse(data=res_body, status=500, message="Error saving user.")
    return CustomResponse(data=res_body, status=200, message="User saved successfully")


@api_view(['POST'])
@permission_classes([AllowAny])
def token(request: Request) -> CustomResponse:
    """
    Login endpoint. Validates credentials, updates login log, retrieves paged permissions,
    and returns a signed JWT access token.
    """
    res_body: Dict[str, Any] = {}
    try:
        username: str = request.data.get("userName", "")
        password: str = request.data.get("password", "")
        
        try:
            admin = Admin.objects.get(userName=username)
        except Admin.DoesNotExist:
            try:
                admin = Admin.objects.get(email=username)
            except Admin.DoesNotExist:
                admin = None
                
        if not admin:
            return CustomResponse(data=res_body, status=500, message="Invalid username or password")
            
        # Cryptographic password verification (supports legacy plain text and BCrypt hashes)
        db_password = admin.password
        is_valid = False
        if db_password.startswith('$2a$') or db_password.startswith('$2b$') or db_password.startswith('$2y$'):
            try:
                is_valid = bcrypt.checkpw(password.encode('utf-8'), db_password.encode('utf-8'))
            except Exception:
                is_valid = False
        else:
            is_valid = (password == db_password)
            
        if not is_valid:
            return CustomResponse(data=res_body, status=500, message="Invalid username or password")
            
        # Emulate getPageNameList and getAdminModulePermissionList via Django ORM
        try:
            pages = AdminPage.objects.all()
            page_list = [p.pgMenuName for p in pages]
            res_body["pageList"] = page_list
            
            module_list = {}
            for p in pages:
                actions = list(AdminPageDetails.objects.filter(pgdPgId=p.pgId).values_list('pgdActionName', flat=True))
                module_list[p.pgMenuName] = actions
            res_body["moduleList"] = module_list
        except Exception:
            res_body["pageList"] = []
            res_body["moduleList"] = {}
            
        admin.lastLoggedIn = timezone.now()
        admin.save()
        
        admin_dto = serialize_admin_dto(admin)
        jwt_token = generate_admin_token(admin)
        
        res_body["token"] = jwt_token
        res_body["member"] = admin_dto
        
    except Exception:
        return CustomResponse(data=res_body, status=500, message="Error during login validation.")
        
    return CustomResponse(data=res_body, status=200, message="Login successful")


@api_view(['POST'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def change_password(request: Request) -> CustomResponse:
    """
    Changes an admin's password after validating the old password securely.
    """
    res_body: Dict[str, Any] = {}
    try:
        member_id: int = request.data.get("memberId")
        old_password: str = request.data.get("password")
        new_password: str = request.data.get("newPassword")
        
        try:
            admin = Admin.objects.get(memberId=member_id)
        except Admin.DoesNotExist:
            return CustomResponse(data=res_body, status=500, message="Old password not matched")
            
        db_password = admin.password
        is_valid = False
        if db_password.startswith('$2a$') or db_password.startswith('$2b$') or db_password.startswith('$2y$'):
            try:
                is_valid = bcrypt.checkpw(old_password.encode('utf-8'), db_password.encode('utf-8'))
            except Exception:
                is_valid = False
        else:
            is_valid = (old_password == db_password)
            
        if not is_valid:
            return CustomResponse(data=res_body, status=500, message="Old password not matched")
            
        hashed_bytes = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
        admin.password = hashed_bytes.decode('utf-8')
        admin.save()
        
    except Exception:
        return CustomResponse(data=res_body, status=500, message="Old password not matched")
        
    return CustomResponse(data=res_body, status=200, message="Password Change Successfully")


@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_admin_list_page(request: Request) -> CustomResponse:
    """
    Gets a paged list of admins based on Pageable page, size, and searchKey.
    """
    res_body: Dict[str, Any] = {}
    try:
        search_key: str = request.query_params.get("searchKey", "")
        
        page_num: int = int(request.query_params.get("page", 0))
        size: int = int(request.query_params.get("size", 10))
        
        if search_key:
            admins = Admin.objects.filter(
                Q(userName__icontains=search_key) |
                Q(firstName__icontains=search_key) |
                Q(lastName__icontains=search_key) |
                Q(email__icontains=search_key)
            )
        else:
            admins = Admin.objects.all()
            
        admins = admins.order_by("memberId")
        
        total_records = admins.count()
        total_pages = (total_records + size - 1) // size if total_records > 0 else 0
        
        offset = page_num * size
        sliced_admins = admins[offset:offset+size]
        
        admin_dto_list = [serialize_admin_dto(a) for a in sliced_admins]
        
        res_body["getTotalPages"] = total_pages
        res_body["getNumber"] = page_num
        res_body["getSize"] = size
        res_body["adminListPage"] = admin_dto_list
        res_body["getTotalRecords"] = total_records
        
    except Exception:
        return CustomResponse(data=res_body, status=500, message="Error in Fetching User List")
        
    return CustomResponse(data=res_body, status=200, message="User List Fetched Successfully")
