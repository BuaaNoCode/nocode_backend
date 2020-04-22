from django.urls import path
from user_manager.api.auth import login
from user_manager.api.user_management import create_user, disable_user, reset_password
urlpatterns = [
    path("", login),
    path("create", create_user),
    path("disable", disable_user),
    path("reset", reset_password)
]
