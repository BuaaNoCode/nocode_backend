from django.contrib.auth import get_user_model
from django.db import models
from common.consts import Everyone, User, VIP, Admin


class UserPermission(models.Model):
    level = [
        (Everyone, "Everyone can access"),
        (User, "Logined user can access"),
        (VIP, "VIP user can access"),
        (Admin, "Only administrators can access")
    ]

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    level = models.IntegerField(choices=level, default=Everyone)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
