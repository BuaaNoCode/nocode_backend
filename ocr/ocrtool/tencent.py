import csv
import json

from django.conf import settings
from qcloud_cos import CosConfig, CosS3Client
from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import \
    TencentCloudSDKException
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.ocr.v20181119 import models, ocr_client

_tencent_bucket_url = r"{}".format(settings.TENCENT_BUCKET_URL)
_tencent_bucket_name = settings.TENCENT_BUCKET_NAME
_tencent_bucket_secret_id = settings.TENCENT_BUCKET_SECRET_ID
_tencent_bucket_secret_key = settings.TENCENT_BUCKET_SECRET_KEY
_tencent_credential_1 = settings.TENCENT_CREDENTIAL_1
_tencent_credential_2 = settings.TENCENT_CREDENTIAL_2


_region = 'ap-beijing'
_token = None
_scheme = 'https'
_config = CosConfig(Region=_region, SecretId=_tencent_bucket_secret_id,
                    SecretKey=_tencent_bucket_secret_key, Token=_token, Scheme=_scheme)


def upload_bucket(file):
    # 获取客户端对象
    client = CosS3Client(_config)
    # 存储在腾讯云的文件名
    picName = r"nocode_pic.jpg"
    # 本地的图片路径
    response = client.put_object(
        Bucket=_tencent_bucket_name,
        Body=file,
        Key=picName,
        StorageClass='STANDARD',
        EnableMD5=False,
        ACL='public-read'
    )
    # 图片在腾讯云的url
    return _tencent_bucket_url+picName


def tencent_ocr_api(url):
    try:
        cred = credential.Credential(_tencent_credential_1, _tencent_credential_2)
        httpProfile = HttpProfile()
        httpProfile.endpoint = "ocr.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = ocr_client.OcrClient(cred, "ap-beijing", clientProfile)

        req = models.TableOCRRequest()
        params = '{"ImageUrl":"%s"}' % url

        req.from_json_string(params)

        resp = client.TableOCR(req)
        r = json.loads(resp.to_json_string())
        texts = r["TextDetections"]
        row = 0
        line = 0
        for text in texts:
            row = max(row, text["RowTl"])
            line = max(line, text["ColTl"])
        dict = {}
        line = line + 1
        row = row + 1
        sheet = [[""] * line for i in range(row)]
        for text in texts:
            sheet[text["RowTl"]][text["ColTl"]] = text["Text"].strip()
        dict["status"] = "succeed"
        dict["row"] = row
        dict["line"] = line
        dict["sheet"] = sheet
        return dict

    except TencentCloudSDKException as err:
        dict = {}
        dict["status"] = "failed"
        dict["err"] = err
        return dict


def tencent_ocr_handler(file):
    url = upload_bucket(file)
    form_info = tencent_ocr_api(url)
    if form_info["status"] == "succeed":
        return True, "\n".join(",".join(form_info["sheet"][i]) for i in range(form_info["row"]))
    else:
        return False, form_info["err"]
