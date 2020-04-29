from django.http import HttpRequest
from django.views.decorators.http import require_http_methods

from common.consts import VIP, User
from common.utils import (StatusCode, failed_api_response, response_wrapper,
                          success_api_response, validate_data)
from ocr.models.project import Project
from ocr.models.recognition_result import RecognitionResult
from user_manager.interface import auth_required
from ocr.ocrtool.form_recognizer_layout import form_recognizer_layout


@response_wrapper
@require_http_methods(["POST"])
@auth_required(VIP)
def receieve_ocr_photo(request: HttpRequest, project_id: int):
    """receieve ocr photo and invoke ocr handler

    [route]: /ocr/project/<int:project_id>

    [method]: POST
    """
    user = request.user
    project: Project = Project.objects.filter(
        id=project_id).filter(belong_to=user).first()
    if not project:
        return failed_api_response(StatusCode.REFUSE_ACCESS)
    
    # TODO:: fetch something from request and pass them to ocr_handler
    json_text = request.FILES.get("json", None)
    load = json.load(json_text)
    rname = load["name"]
    rcomment = load["comment"]
    img_file = request.FILES.get("file", None)

    result_json = ocr_handler(img_file)
    result: RecognitionResult = RecognitionResult(
        name = rname,
        comment = rcomment,
        belong_to = project,
        result = result_json
    )
    result.save()

    res_data = {
        "id": result.id,
        "created_at": result.created_at
    }
    return success_api_response(res_data)


def ocr_handler(img_file):
    source = ""
    r_json = form_recognizer_layout(source, img_file, img_file.content_type)
    return r_json


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

    result: RecognitionResult = project.recognitionresult.filter(
        id=result_id).first()
    if not result:
        return failed_api_response(StatusCode.ITEM_NOT_FOUND)

    res_data = {
        "id": result.id,
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

    result: RecognitionResult = project.recognitionresult.filter(
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

    result: RecognitionResult = project.recognitionresult.filter(
        id=result_id).first()
    if not result:
        return failed_api_response(StatusCode.ITEM_NOT_FOUND)

    result.delete()
    return success_api_response({"result": "Ok, Recognition result removed"})
