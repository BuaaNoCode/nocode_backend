import base64
import time

from django.conf import settings
import requests


_access_token_url = r"{}".format(settings.BAIDU_ACCESS_TOKEN)

def getAccessToken():
    response = requests.get(_access_token_url)
    acc_token = response.json()['access_token']
    return acc_token


def ocr_get_result(acc_token, request_id, url, result_type):
    # result_type: excel or json
    params = {"request_id": request_id, "result_type": result_type}
    access_token = acc_token
    request_url = url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}

    n_tries = 10
    n_try = 0
    wait_sec = 5
    while n_try < n_tries:
        response = requests.post(request_url, data=params, headers=headers)
        response_json = response.json()
        print(response_json)
        if not response_json.get("result"):
            return False, {"error": {"code": "AnalysisFailed", "message": "Analysis failed"}}
        if response_json["result"]["ret_code"] == 3:
            return True, response.json()
        time.sleep(wait_sec)
    return False, {"error": {"code": "AnalysisFailed", "message": "Analysis not finished in time"}}


def analyseFormForBaidu(file, result_type):
    img = base64.b64encode(file.read())

    access_token = getAccessToken()

    url_request = "https://aip.baidubce.com/rest/2.0/solution/v1/form_ocr/request"
    request_url = url_request + "?access_token=" + access_token

    headers = {'content-type': 'application/x-www-form-urlencoded'}
    params = {"image": img}

    response = requests.post(request_url, data=params, headers=headers)
    result_id = response.json()['result'][0]['request_id']

    return ocr_get_result(access_token, result_id,
                          "https://aip.baidubce.com/rest/2.0/solution/v1/form_ocr/get_request_result", result_type)