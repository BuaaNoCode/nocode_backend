from common.utils import wrapped_api

from .ocr_result import (receive_ocr_photo, remove_ocr_result,
                         retrieve_ocr_result, update_ocr_result)
from .project import (create_project, list_projects, remove_project,
                      retrieve_project_detail, update_project)

PROJECT_API = wrapped_api({
    "post": create_project,
    "get": list_projects
})

PROJECT_DETAIL_API = wrapped_api({
    "post": receive_ocr_photo,
    "put": update_project,
    "get": retrieve_project_detail,
    "delete": remove_project
})

RESULT_DETAIL_API = wrapped_api({
    "get": retrieve_ocr_result,
    "put": update_ocr_result,
    "delete": remove_ocr_result
})
