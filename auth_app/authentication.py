import jwt
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from common_app.models import Admin, Member
from common_app.common_variable import CommonVariable
from auth_app.utils import decode_token

class CustomJWTAuthentication(BaseAuthentication):
    """
    Custom Django REST Framework Authentication class.
    Migrates request filtering and validation logic from Spring Boot's
    JwtRequestFilter.java and CustomAuthenticateManager.java.
    """

    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            raise AuthenticationFailed('Authorization header is missing.')

        if not auth_header.startswith('Bearer '):
            raise AuthenticationFailed('Authorization header must start with "Bearer ".')

        # Extract the raw token string
        token = auth_header[7:]

        try:
            # Decode and validate token signatures and expiration
            payload = decode_token(token)
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired.')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token.')

        username = payload.get('sub')
        member_id = payload.get('memberId')

        if not username:
            raise AuthenticationFailed('Token does not contain a subject (sub) claim.')

        # Maintain global MEMBERID reference in CommonVariable for backward compatibility
        if member_id is not None:
            CommonVariable.MEMBERID = member_id

        user = None

        # 1. Attempt to fetch from Admin table (using admin_name or email)
        try:
            user = Admin.objects.get(userName=username)
        except Admin.DoesNotExist:
            try:
                user = Admin.objects.get(email=username)
            except Admin.DoesNotExist:
                pass

        # 2. Attempt to fetch from Member table if not found in Admin
        if not user:
            try:
                user = Member.objects.get(username=username)
            except Member.DoesNotExist:
                try:
                    user = Member.objects.get(email=username)
                except Member.DoesNotExist:
                    pass

        # 3. Fallback search by member_id if present
        if not user and member_id is not None:
            try:
                user = Member.objects.get(memberId=member_id)
            except Member.DoesNotExist:
                try:
                    user = Admin.objects.get(memberId=member_id)
                except Admin.DoesNotExist:
                    pass

        if not user:
            raise AuthenticationFailed('User matching token credentials not found.')

        return (user, token)
