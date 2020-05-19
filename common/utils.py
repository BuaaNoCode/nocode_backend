import json
import random
import string
from enum import Enum

from django.db.models import Model
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


def validate_data(fields: list):
    def decorator(func):
        def inner(request, *args, **kwargs):
            data: dict = parse_data(request)
            if data is None or not isinstance(data, dict):
                return failed_api_response(StatusCode.INVALID_REQUEST_ARGUMENT)
            if not set(data.keys()) <= set(fields):
                return failed_api_response(StatusCode.INVALID_REQUEST_ARGUMENT)
            kwargs["data"] = data
            return func(request, *args, **kwargs)
        return inner
    return decorator


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


def wrapped_api(api_dict: dict):
    api_dict = {k.upper(): v for k, v in api_dict.items()}

    @require_http_methods(api_dict.keys())
    def api(request, *args, **kwargs):
        return api_dict[request.method](request, *args, **kwargs)
    return api


def api_record(model: Model, api, user: bool):
    def decorator(func):
        def inner(request, *args, **kwargs):
            if user:
                record = model.objects.get_or_create(
                    api=api.value, user=request.user)[0]
            else:
                record = model.objects.get_or_create(api=api.value)[0]
            record.call_count = record.call_count + 1
            record.save()
            return func(request, *args, **kwargs)
        return inner
    return decorator


def dump_api_record(model: Model, ApiIndex: Enum):
    result = {}
    for api in ApiIndex:
        records = model.objects.filter(api=api.value)
        result[api.value] = {
            "num": len(records),
            "detail": list(records.values("count", "user"))
        }
    return result


def random_str(length):
    return "".join(random.sample(string.ascii_letters + string.digits, length))
