import json
import time

from django.conf import settings
from requests import get, post

_azure_endpoint = r"{}".format(settings.AZURE_ENDPOINT)
_azure_apim_key = settings.AZURE_APIM_KEY


def azure_form_recognizer_layout(files, content_type):
    post_url = _azure_endpoint + "/formrecognizer/v2.0-preview/Layout/analyze"
    headers = {
        'Content-Type': content_type,
        'Ocp-Apim-Subscription-Key': _azure_apim_key,
    }
    data_bytes = files.read()
    try:
        resp = post(url=post_url, data=data_bytes, headers=headers)
        if resp.status_code != 202:
            return False, json.loads(resp.text)
        get_url = resp.headers["operation-location"]
    except Exception as e:
        return False, json.loads(('{"error":{"code":"POSTUnkownError", "message":"'+str(e)+'"}}'))
    n_tries = 10
    n_try = 0
    wait_sec = 6
    while n_try < n_tries:
        try:
            resp = get(url=get_url, headers={"Ocp-Apim-Subscription-Key": _azure_apim_key})
            resp_json = json.loads(resp.text)
            if resp.status_code != 200:
                return False, resp_json
            status = resp_json["status"]
            if status == "succeeded":
                return True, resp_json
            if status == "failed":
                return False, json.loads('{"error":{"code":"AnalysisFailed", "message":"Can\'t analyze"}}')
            time.sleep(wait_sec)
            n_try += 1
        except Exception as e:
            return False, json.loads(('{"error":{"code":"GETUnkownError", "message":"' + str(e) + '"}}'))
    return False, json.loads(('{"error":{"code":"GETTimeLimitExceeded", "message":"may try later"}}'))
