from django.urls import path

from .api import (LOGIN_API, USER_CREATE_API, USER_DISABLE_API,
                              USER_RESET_API)

urlpatterns = [
    path("", LOGIN_API),
    path("create", USER_CREATE_API),
    path("disable", USER_DISABLE_API),
    path("reset", USER_RESET_API)
]
