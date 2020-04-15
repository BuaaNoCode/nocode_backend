from django.contrib.auth import get_user_model
from django.http import HttpRequest
from django.views.decorators.http import require_http_methods

from common.consts import StatusCode
from common.utils import (failed_api_response, parse_data, response_wrapper,
                          success_api_response)

UserModel = get_user_model()


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
    if username is None or password is None or email is None:
        return failed_api_response(StatusCode.INVALID_REQUEST_ARGUMENT, "Bad user information")
    if UserModel.objects.filter(username=username).exists():
        return failed_api_response(StatusCode.ITEM_ALREADY_EXISTS, "Username conflicted")

    new_user = UserModel.objects.create_user(
        username=username, password=password, email=email)

    return success_api_response({"id": new_user.id})



@response_wrapper
@require_http_methods(["POST"])
def delete_user(request: HttpRequest):
    """delete user

    [route]: /auth/delete

    [method]: POST
    """
    user_info: dict = parse_data(request)
    if not user_info:
        return failed_api_response(StatusCode.BAD_REQUEST, "Bad request")
    username = user_info.get("username")
    password = user_info.get("password")
    email = user_info.get("email")
    if username is None or password is None or email is None:
        return failed_api_response(StatusCode.INVALID_REQUEST_ARGUMENT, "Bad user information")
    if not UserModel.objects.filter(username=username).exists():
        return failed_api_response(StatusCode.ITEM_NOT_FOUND, "Username does not exists")

    user = UserModel.objects.get(username=username)
    user.delete()

    return success_api_response({"id": user.id})


