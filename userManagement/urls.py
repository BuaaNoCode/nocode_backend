from django.urls import path
from userManagement.api.auth import login
from userManagement.api.user_management import create_user
urlpatterns = [
    path("", login),
    path("create", create_user)
]
