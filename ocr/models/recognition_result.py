from django.db import models
from django.contrib.auth import get_user_model
from ocr.models.project import Project


OCR_NONE_BOTTOM = 0  # Bad status
OCR_AZURE = 1
OCR_BAIDU = 2
OCR_TENCENT = 3
OCR_NONE_TOP = 4  # Bad status


class RecognitionResult(models.Model):
    OCR_TYPE = [
        (OCR_NONE_BOTTOM, "None Bottom"),
        (OCR_AZURE, "Azure"),
        (OCR_BAIDU, "Baidu"),
        (OCR_TENCENT, "Tencent"),
        (OCR_NONE_TOP, "None Top"),
    ]
    name = models.CharField(max_length=50, default="")
    comment = models.TextField(default="")
    belong_to = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    ocr_type = models.IntegerField(default=OCR_NONE_BOTTOM, choices=OCR_TYPE)
    result = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True)
