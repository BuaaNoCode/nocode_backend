from django.urls import path

from .api import PROJECT_API, PROJECT_DETAIL_API, RESULT_DETAIL_API

urlpatterns = [
    path("project", PROJECT_API),
    path("project/<int:project_id>", PROJECT_DETAIL_API),
    path("project/<int:project_id>/<int:result_id>", RESULT_DETAIL_API)
]
