import json
from enum import Enum

from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_http_methods

from common.consts import StatusCode


def response_wrapper(func):
    def inner(*args, **kwargs):
        response = func(*args, **kwargs)
        if isinstance(response, dict):
            if response["success"]:
                response = JsonResponse(response["data"])
            else:
                status_code = response.get("data").get("code")
                response = JsonResponse(response["data"])
                response.status_code = status_code
        return response

    return inner


def api_response(success, data) -> dict:
    return {"success": success, "data": data}


def failed_api_response(code: StatusCode, error_msg=None) -> dict:
    if error_msg is None:
        error_msg = str(code)
    else:
        error_msg = str(code) + ": " + error_msg

    status_code = code.value // 100
    detailed_code = code.value
    return api_response(
        success=False,
        data={
            "code": status_code,
            "detailed_error_code": detailed_code,
            "error_msg": error_msg
        })


def success_api_response(data) -> dict:
    return api_response(True, data)

def parse_data(request: HttpRequest):
    try:
        return json.loads(request.body.decode())
    except json.JSONDecodeError:
        return None
