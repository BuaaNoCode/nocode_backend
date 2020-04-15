from django.urls import path
from auth.api.auth import login
from auth.api.user_management import create_user
urlpatterns = [
    path("", login),
    path("create", create_user),
    path("delete", delete_user),
    path("change_password", change_password)
]
