from django.db import models
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class OCRApiRecord(models.Model):
    api = models.IntegerField()
    user = models.ForeignKey(to=UserModel, on_delete=models.CASCADE, null=True)
    count = models.IntegerField(default=0)
