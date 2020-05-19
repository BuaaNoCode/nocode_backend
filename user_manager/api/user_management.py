from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.http import HttpRequest
from django.views.decorators.http import require_http_methods

from common.consts import StatusCode, User
from common.utils import (failed_api_response, parse_data, random_str,
                          response_wrapper, success_api_response)
from user_manager.api.auth import auth_required
from user_manager.forms.email import VerifiedEmail
from user_manager.forms.user import VerifiedUserForm

UserModel = get_user_model()


@response_wrapper
@require_http_methods(["POST"])
def send_captcha(request: HttpRequest):
    """create captcha before registration or reset password

    [route]: /auth/captcha

    [method]: POST
    """
    email_info: dict = parse_data(request)
    if not email_info:
        return failed_api_response(StatusCode.BAD_REQUEST, "Bad request")
    email = email_info.get("email")
    verified_form = VerifiedEmail({"email": email})
    if not verified_form.is_valid():
        return failed_api_response(StatusCode.INVALID_REQUEST_ARGUMENT, "Bad email address")
    captcha = random_str(6)
    cache.set(email, captcha, 5 * 60)
    # TODO:: Send Email
    return success_api_response({"result": "Ok, confirmation email has been sent"})


@response_wrapper
@require_http_methods(["POST"])
def create_user(request: HttpRequest):
    """create user

    [route]: /auth/create

    [method]: POST
    """
    user_info: dict = parse_data(request)
    if not user_info:
        return failed_api_response(StatusCode.BAD_REQUEST, "Bad request")
    username = user_info.get("username")
    password = user_info.get("password")
    email = user_info.get("email")
    captcha = user_info.get("captcha")
    verified_form = VerifiedUserForm({
        "username": username,
        "password": password,
        "email": email,
        "captcha": captcha
    })
    if not verified_form.is_valid():
        return failed_api_response(StatusCode.INVALID_REQUEST_ARGUMENT, "Bad information")
    verified_captcha = cache.get(email)
    delattr(cache, email)
    if captcha != verified_captcha:
        return failed_api_response(StatusCode.INVALID_CAPTCHA, "Captcha not matched")
    if UserModel.objects.filter(username=username).exists():
        return failed_api_response(StatusCode.ITEM_ALREADY_EXISTS, "Username conflicted")

    new_user = UserModel.objects.create_user(
        username=username, password=password, email=email)

    return success_api_response({"id": new_user.id})


@response_wrapper
@auth_required(User)
@require_http_methods(["POST"])
def disable_user(request: HttpRequest):
    """disable user

    [route]: /auth/disable

    [method]: POST
    """
    user_info: dict = parse_data(request)
    if not user_info:
        return failed_api_response(StatusCode.BAD_REQUEST, "Bad request")
    username = user_info.get("username")
    password = user_info.get("password")
    if username is None or password is None:
        return failed_api_response(StatusCode.INVALID_REQUEST_ARGUMENT, "Bad user information")
    if not UserModel.objects.filter(username=username).exists():
        return failed_api_response(StatusCode.ITEM_NOT_FOUND, "User does not exist")

    user = UserModel.objects.get(username=username)

    if not user.check_password(password):
        return failed_api_response(StatusCode.INVALID_USERNAME_OR_PASSWORD, "User password is wrong")

    user.is_active = False
    user.save()

    return success_api_response({"result": "Ok, user has been diabled."})


@response_wrapper
@auth_required(User)
@require_http_methods(["POST"])
def reset_password(request: HttpRequest):
    """reset user password

    [route]: /auth/reset

    [method]: POST
    """
    user_info: dict = parse_data(request)
    if not user_info:
        return failed_api_response(StatusCode.BAD_REQUEST, "Bad request")
    username = user_info.get("username")
    password = user_info.get("password")
    new_password = user_info.get("new_password")
    if username is None or password is None or new_password is None:
        return failed_api_response(StatusCode.INVALID_REQUEST_ARGUMENT, "Bad user information")
    if not UserModel.objects.filter(username=username).exists():
        return failed_api_response(StatusCode.ITEM_NOT_FOUND, "User does not exist")

    user = UserModel.objects.get(username=username)

    if not user.check_password(password):
        return failed_api_response(StatusCode.INVALID_USERNAME_OR_PASSWORD, "User password is wrong")

    user.set_password(new_password)
    user.save()

    return success_api_response({"result": "Ok, password has been updated."})


@response_wrapper
@require_http_methods(["POST"])
def forgot_password(request: HttpRequest):
    """forgot password and reset

    [route]: /auth/forgot

    [method]: POST
    """
    user_info: dict = parse_data(request)
    if not user_info:
        return failed_api_response(StatusCode.BAD_REQUEST, "Bad request")
    username = user_info.get("username")
    password = user_info.get("password")
    email = user_info.get("email")
    captcha = user_info.get("captcha")
    verified_form = VerifiedUserForm({
        "username": username,
        "password": password,
        "email": email,
        "captcha": captcha
    })
    if not verified_form.is_valid():
        return failed_api_response(StatusCode.INVALID_REQUEST_ARGUMENT, "Bad information")
    verified_captcha = cache.get(email)
    delattr(cache, email)
    if captcha != verified_captcha:
        return failed_api_response(StatusCode.INVALID_CAPTCHA, "Captcha not matched")
    user = UserModel.objects.filter(username=username).first()
    if not user or user.email != email:
        return failed_api_response(StatusCode.ITEM_NOT_FOUND, "User not found")
    user.set_password(password)
    user.save()

    return success_api_response({"result": "Ok, password reset"})
