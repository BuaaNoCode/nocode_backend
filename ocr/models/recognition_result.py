from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField
from ocr.models.project import Project

class RecognitionResult(models.Model):
    name = models.CharField(max_length=50, default="")
    comment = models.TextField(default="")
    belong_to = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    result = JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
