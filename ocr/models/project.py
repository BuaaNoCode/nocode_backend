from django.db import models
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class Project(models.Model):
    name = models.CharField(max_length=50, default="")
    comment = models.TextField(default="")
    belong_to = models.ForeignKey(to=UserModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
