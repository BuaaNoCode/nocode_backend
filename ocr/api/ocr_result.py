import json
from enum import Enum

from django.http import HttpRequest
from django.views.decorators.http import require_http_methods

from common.consts import VIP, User
from common.utils import (StatusCode, api_record, failed_api_response,
                          response_wrapper, success_api_response,
                          validate_data)
from ocr.models.ocr_api_record import OCRApiRecord
from ocr.models.project import Project
from ocr.models.recognition_result import *
from ocr.ocrtool.azure import azure_form_recognizer_layout
from ocr.ocrtool.baidu import analyseFormForBaidu
from ocr.ocrtool.tencent import tencent_ocr_handler
from user_manager.interface import auth_required


class ApiIndex(Enum):
    RECEIVE_OCR_PHOTO = 1


@response_wrapper
@require_http_methods(["POST"])
@auth_required(User)
@api_record(model=OCRApiRecord, api=ApiIndex.RECEIVE_OCR_PHOTO, user=True)
def receive_ocr_photo(request: HttpRequest, project_id: int):
    """receive ocr photo and invoke ocr handler

    [route]: /ocr/project/<int:project_id>

    [method]: POST
    """
    user = request.user
    project: Project = Project.objects.filter(
        id=project_id).filter(belong_to=user).first()
    if not project:
        return failed_api_response(StatusCode.REFUSE_ACCESS)
    json_text = request.POST.get("json", None)
    img_file = request.FILES.get("file", None)
    load = json.loads(json_text)
    name = load.get("name")
    comment = load.get("comment")
    result_json = azure_ocr_handler(img_file)
    result: RecognitionResult = RecognitionResult(
        name=name,
        comment=comment,
        belong_to=project,
        result=result_json
    )
    result.save()
    res_data = {
        "id": result.id,
        "created_at": result.created_at
    }
    return success_api_response(res_data)


@response_wrapper
@require_http_methods(["POST"])
@auth_required(User)
def handle_ocr_photo(request: HttpRequest, project_id: int, result_id: int):
    """receive ocr request and invoke ocr handler

    [route]: /ocr/project/<int:project_id>/<int:result_id>

    [method]: POST
    """
    user = request.user
    project: Project = Project.objects.filter(
        id=project_id).filter(belong_to=user).first()
    if not project:
        return failed_api_response(StatusCode.REFUSE_ACCESS)

    result: RecognitionResult = project.recognitionresult_set.filter(
        id=result_id).first()
    if not result:
        return failed_api_response(StatusCode.ITEM_NOT_FOUND)

    img_file = request.FILES.get("file", None)
    if img_file is None:
        return failed_api_response(StatusCode.NO_IMAGE_FILE)

    result_string = ""
    status = True
    ocr_type = result.ocr_type
    if ocr_type == OCR_AZURE:
        status, result_string = azure_ocr_handler(img_file)
    elif ocr_type == OCR_BAIDU:
        status, result_string = baidu_handler(img_file)
    elif ocr_type == OCR_TENCENT:
        status, result_string = tencent_handler(img_file)

    result.result = result_string


def azure_ocr_handler(img_file):
    status, resp_json = azure_form_recognizer_layout(img_file, img_file.content_type)
    return status, json.dumps(resp_json)


def baidu_handler(img_file):
    return analyseFormForBaidu(img_file, "json")


def tencent_handler(img_file):
    return tencent_ocr_handler(img_file)


@response_wrapper
@require_http_methods(["POST"])
@auth_required(User)
@validate_data(fields=["name", "comment", "ocr_type"])
def create_ocr_result(request: HttpRequest, project_id: int, **kwargs):
    """create ocr result before uploading photo

    [route]: /ocr/project/<int:project_id>

    [method]: POST
    """
    user = request.user
    project: Project = Project.objects.filter(
        id=project_id).filter(belong_to=user).first()
    if not project:
        return failed_api_response(StatusCode.REFUSE_ACCESS)
    info: dict = kwargs.get("data")
    name = info.get("name", "")
    comment = info.get("comment", "")
    ocr_type = info.get("ocr_type")

    if ocr_type is None or not isinstance(ocr_type, int) or not OCR_NONE_BOTTOM < ocr_type < OCR_NONE_TOP:
        return failed_api_response(StatusCode.BAD_OCR_TYPE)

    result: RecognitionResult = RecognitionResult(
        name=name,
        comment=comment,
        ocr_type=ocr_type,
        belong_to=user
    )
    result.save()

    return success_api_response({
        "id": result.id,
        "created_at": result.created_at
    })


@response_wrapper
@require_http_methods(["GET"])
@auth_required(User)
def retrieve_ocr_result(request: HttpRequest, project_id: int, result_id: int):
    """retrieve ocr result

    [route]: /ocr/project/<int:project_id>/<int:result_id>

    [method]: GET
    """
    user = request.user
    project: Project = Project.objects.filter(
        id=project_id).filter(belong_to=user).first()
    if not project:
        return failed_api_response(StatusCode.REFUSE_ACCESS)

    result: RecognitionResult = project.recognitionresult_set.filter(
        id=result_id).first()
    if not result:
        return failed_api_response(StatusCode.ITEM_NOT_FOUND)

    res_data = {
        "id": result.id,
        "name": result.name,
        "comment": result.comment,
        "result": result.result
    }
    return success_api_response(res_data)


@response_wrapper
@require_http_methods(["PUT"])
@auth_required(User)
@validate_data(fields=["name", "comment"])
def update_ocr_result(request: HttpRequest, project_id: int, result_id: int, **kwargs):
    """retrieve ocr result

    [route]: /ocr/project/<int:project_id>/<int:result_id>

    [method]: GET
    """
    user = request.user
    project: Project = Project.objects.filter(
        id=project_id).filter(belong_to=user).first()
    if not project:
        return failed_api_response(StatusCode.REFUSE_ACCESS)

    result: RecognitionResult = project.recognitionresult_set.filter(
        id=result_id).first()
    if not result:
        return failed_api_response(StatusCode.ITEM_NOT_FOUND)

    data: dict = kwargs.get("data")
    for key in data.keys():
        setattr(result, key, data.get(key))
    result.save()
    return success_api_response({"result": "Ok, Recognition result updated"})


@response_wrapper
@require_http_methods(["DELETE"])
@auth_required(User)
def remove_ocr_result(request: HttpRequest, project_id: int, result_id: int):
    """remove ocr result

    [route]: /ocr/project/<int:project_id>/<int:result_id>

    [method]: DELETE
    """
    user = request.user
    project: Project = Project.objects.filter(
        id=project_id).filter(belong_to=user).first()
    if not project:
        return failed_api_response(StatusCode.REFUSE_ACCESS)

    result: RecognitionResult = project.recognitionresult_set.filter(
        id=result_id).first()
    if not result:
        return failed_api_response(StatusCode.ITEM_NOT_FOUND)

    result.delete()
    return success_api_response({"result": "Ok, Recognition result removed"})
