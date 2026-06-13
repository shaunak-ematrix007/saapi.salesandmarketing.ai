import datetime
import jwt
from django.conf import settings

def generate_token(member_id, first_name, last_name, subject, expires_in_hours=10):
    """
    Generates a JWT token using HS256 algorithm with matching claims structure from Java:
    - memberId
    - firstName
    - lastName
    - sub (subject)
    - iat (issued at)
    - exp (expiration)
    """
    now = datetime.datetime.utcnow()
    payload = {
        'memberId': member_id,
        'firstName': first_name,
        'lastName': last_name,
        'sub': subject,
        'iat': now,
        'exp': now + datetime.timedelta(hours=expires_in_hours)
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm='HS256')

def generate_admin_token(admin_user, expires_in_hours=10):
    """
    Generates a token for an Admin.
    Expects admin_user to be an object (or dictionary) with memberId, firstName, lastName, and userName.
    """
    if isinstance(admin_user, dict):
        member_id = admin_user.get('memberId') or admin_user.get('member_id')
        first_name = admin_user.get('firstName') or admin_user.get('first_name')
        last_name = admin_user.get('lastName') or admin_user.get('last_name')
        subject = admin_user.get('userName') or admin_user.get('username') or admin_user.get('email')
    else:
        member_id = getattr(admin_user, 'memberId', getattr(admin_user, 'member_id', None))
        first_name = getattr(admin_user, 'firstName', getattr(admin_user, 'first_name', None))
        last_name = getattr(admin_user, 'lastName', getattr(admin_user, 'last_name', None))
        subject = getattr(admin_user, 'userName', getattr(admin_user, 'username', getattr(admin_user, 'email', None)))

    return generate_token(member_id, first_name, last_name, subject, expires_in_hours)

def generate_member_token(member_user, expires_in_hours=10):
    """
    Generates a token for a Member.
    Expects member_user to be an object (or dictionary) with memberId, firstName, lastName, and email.
    """
    if isinstance(member_user, dict):
        member_id = member_user.get('memberId') or member_user.get('member_id')
        first_name = member_user.get('firstName') or member_user.get('first_name')
        last_name = member_user.get('lastName') or member_user.get('last_name')
        subject = member_user.get('email') or member_user.get('userName') or member_user.get('username')
    else:
        member_id = getattr(member_user, 'memberId', getattr(member_user, 'member_id', None))
        first_name = getattr(member_user, 'firstName', getattr(member_user, 'first_name', None))
        last_name = getattr(member_user, 'lastName', getattr(member_user, 'last_name', None))
        subject = getattr(member_user, 'email', getattr(member_user, 'userName', getattr(member_user, 'username', None)))

    return generate_token(member_id, first_name, last_name, subject, expires_in_hours)

def decode_token(token):
    """
    Decodes the token using the configured JWT_SECRET_KEY.
    Raises jwt.ExpiredSignatureError if the token is expired.
    Raises jwt.InvalidTokenError for all other invalid signature/decoding errors.
    """
    return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=['HS256'])

def extract_username(token):
    """
    Extracts the subject (username or email) from the token.
    Returns None if decoding fails.
    """
    try:
        payload = decode_token(token)
        return payload.get('sub')
    except jwt.InvalidTokenError:
        return None

def extract_member_id(token):
    """
    Extracts the memberId claim from the token.
    Returns None if decoding fails.
    """
    try:
        payload = decode_token(token)
        member_id = payload.get('memberId')
        return int(member_id) if member_id is not None else None
    except (jwt.InvalidTokenError, ValueError, TypeError):
        return None

def extract_expiration(token):
    """
    Extracts the expiration datetime from the token.
    Returns None if decoding fails.
    """
    try:
        # We need to decode without verifying expiration to get the exp claim of expired tokens
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=['HS256'], options={"verify_exp": False})
        exp_timestamp = payload.get('exp')
        if exp_timestamp is not None:
            return datetime.datetime.utcfromtimestamp(exp_timestamp)
        return None
    except jwt.InvalidTokenError:
        return None

def is_token_expired(token):
    """
    Checks if the token's expiration has passed.
    """
    try:
        decode_token(token)
        return False
    except jwt.ExpiredSignatureError:
        return True
    except jwt.InvalidTokenError:
        return True

def validate_token(token, expected_username):
    """
    Validates that the token's subject matches the expected username/email
    and that the token is not expired.
    """
    try:
        payload = decode_token(token)
        username = payload.get('sub')
        return username == expected_username
    except jwt.InvalidTokenError:
        return False
