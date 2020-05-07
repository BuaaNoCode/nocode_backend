from datetime import timedelta

import jwt
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.db.models import Q
from django.http import HttpRequest
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from common.consts import Everyone, User
from common.utils import (StatusCode, failed_api_response, parse_data,
                          response_wrapper, success_api_response)
from user_manager.models.permission_level import UserPermission

UserModel = get_user_model()


def auth_failed(status: StatusCode, msg: str):
    return failed_api_response(status, msg)


def generate_access_token(user_id: int, valid_hours: int = 24) -> str:
    current_time = timezone.now()
    access_token_payload = {
        "user_id": user_id,
        "exp": current_time + timedelta(hours=valid_hours),
        "iat": current_time,
        "type": "access_token",
    }
    return jwt.encode(access_token_payload, settings.SECRET_KEY, algorithm="HS256").decode("utf-8")


@response_wrapper
@require_http_methods(["POST"])
def login(request: HttpRequest):
    """Handle requests which are to obtain jwt token

    [route]: /auth/

    [method]: POST
    """
    data: dict = parse_data(request)
    if not data or data.get("username") is None or data.get("password") is None:
        return failed_api_response(StatusCode.INVALID_REQUEST_ARGUMENT, "Bad login info")
    user = authenticate(username=data["username"], password=data["password"])
    if not user:
        return failed_api_response(StatusCode.INVALID_USERNAME_OR_PASSWORD, "The username or password is incorrect")
    return success_api_response({
        "access_token": generate_access_token(user.id)
    })


def verify_jwt_token(request: HttpRequest) -> (bool, StatusCode, str, int):
    flag: bool = True
    msg: str = ""
    user_id: int = -1
    status: StatusCode = StatusCode.SUCCESS
    header: str = request.META.get("HTTP_AUTHORIZATION")
    try:
        if header is None:
            raise jwt.InvalidTokenError

        auth_info = header.split(" ")
        if len(auth_info) != 2:
            raise jwt.InvalidTokenError
        auth_type, auth_token = auth_info

        if auth_type != "Bearer":
            raise jwt.InvalidTokenError
        token = jwt.decode(auth_token, settings.SECRET_KEY, algorithms="HS256")
        if token.get("type") != "access_token":
            raise jwt.InvalidTokenError
        user_id = int(token["user_id"])
    except jwt.ExpiredSignatureError:
        flag, status, msg = False, StatusCode.TOKEN_EXPIRED, "Token expired"
    except jwt.InvalidTokenError:
        flag, status, msg = False, StatusCode.INVALID_TOKEN, "Invalid token"
    return (flag, status, msg, user_id)


def auth_required(level: int):
    def decorator(func):
        def wrapper(request: HttpRequest, *args, **kwargs):
            if level != Everyone:
                (flag, status, msg, user_id) = verify_jwt_token(request)
                if not flag:
                    return auth_failed(status, msg)
                request_user = UserModel.objects.filter(pk=user_id).first()
                if request_user is None:
                    return auth_failed(StatusCode.ACCOUNT_DISABLED, "Sorry, your account has been disabled")
                request.user = request_user
                if level > User and not UserPermission.objects.filter(Q(user__id=user_id) &
                                                                      Q(level__gte=level) &
                                                                      Q(created_at__lt=timezone.now()) &
                                                                      Q(expires_at__gt=timezone.now())).exists():
                    return auth_failed(StatusCode.PERMISSION_DENIED, "Permission denied")
            return func(request, *args, **kwargs)
        return wrapper
    return decorator
