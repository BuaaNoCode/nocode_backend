from django.db.models import Count
from django.http import HttpRequest
from django.views.decorators.http import require_http_methods

from common.consts import VIP, StatusCode, User
from common.utils import (failed_api_response, parse_data, response_wrapper,
                          success_api_response, validate_data)
from ocr.models.project import Project
from user_manager.interface import auth_required


@response_wrapper
@require_http_methods(["POST"])
@auth_required(User)
@validate_data(fields=["name", "comment"])
def create_project(request: HttpRequest, **kwargs):
    """create project

    [route]: /ocr/project

    [method]: POST
    """
    name = kwargs.get("name")
    comment = kwargs.get("comment")

    if len(name) == 0:
        return failed_api_response(StatusCode.INVALID_REQUEST_ARGUMENT, "Project name is required")

    # project: Project = Project.objects.create({
    #     "name": name,
    #     "comment": comment,
    #     "belong_to": request.user
    # })
    project: Project = Project(
        name = name,
        comment = comment,
        belong_to = request.user
    )

    project.save()

    return success_api_response({
        "id": project.id,
        "created_at": project.created_at
    })


@response_wrapper
@require_http_methods(["PUT"])
@auth_required(User)
@validate_data(fields=["name", "comment"])
def update_project(request: HttpRequest, project_id: int, **kwargs):
    """update project

    [route]: /ocr/project/<int:project_id>

    [method]: PUT
    """
    project = Project.objects.filter(id=project_id).first()
    if not project:
        return failed_api_response(StatusCode.ITEM_NOT_FOUND, "Project not found")
    data: dict = kwargs.get("data")
    if data.get("name") and len(data.get("name")) == 0:
        return failed_api_response(StatusCode.INVALID_REQUEST_ARGUMENT, "Project name should not be empty")

    for key in data.keys():
        setattr(project, key, data.get(key))
    project.save()
    return success_api_response({"result": "Ok, Project updated"})


@response_wrapper
@require_http_methods(["GET"])
@auth_required(User)
def list_projects(request: HttpRequest):
    """list user's projects

    [route]: /ocr/project

    [method]: GET
    """
    user = request.user
    projects = Project.objects.filter(belong_to=user).annotate(
        results_num=Count("recognitionresult"))
    res_data = {
        "project_num": projects.count(),
        "projects": list(projects.values("id", "name", "comment", "created_at", "results_num"))
    }

    return success_api_response(res_data)


@response_wrapper
@require_http_methods(["GET"])
@auth_required(User)
def retrieve_project_detail(request: HttpRequest, project_id: int):
    """retrieve a projects' info

    [route]: /ocr/project/<int:project_id>

    [method]: GET
    """
    user = request.user
    project: Project = Project.objects.filter(
        id=project_id).filter(belong_to=user).first()
    if not project:
        return failed_api_response(StatusCode.REFUSE_ACCESS)
    results = project.recognitionresult
    res_data = {
        "name": project.name,
        "comment": project.comment,
        "created_at": project.created_at,
        "result_num": results.count(),
        "results": list(results.values("id", "name", "comment", "created_at"))
    }

    return success_api_response(res_data)


@response_wrapper
@require_http_methods(["DELETE"])
@auth_required(User)
def remove_project(request: HttpRequest, project_id: int):
    """remove a project

    [route]: /ocr/project/<int:project_id>

    [method]: DELETE
    """
    user = request.user
    project: Project = Project.objects.filter(
        id=project_id).filter(belong_to=user).first()
    if not project:
        return failed_api_response(StatusCode.REFUSE_ACCESS)

    project.delete()
    return success_api_response({"result": "Ok, Project removed"})
