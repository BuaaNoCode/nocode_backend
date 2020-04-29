########### Python Form Recognizer Async Layout #############
import json
import time
from requests import get, post

def form_recognizer_layout(source, files, content_type):
    # Endpoint URL
    endpoint = r" https://nocode-form-2.cognitiveservices.azure.com"
    apim_key = "your key"
    post_url = endpoint + "/formrecognizer/v2.0-preview/Layout/analyze"
    headers = {
        # Request headers
        'Content-Type': content_type,
        'Ocp-Apim-Subscription-Key': apim_key,
    }
    if headers['Content-Type'] == 'application/json':
        data_bytes = {"source": source}
    else:
        data_bytes = files.read()
    try:
        resp = post(url = post_url, data = data_bytes, headers = headers)
        if resp.status_code != 202:
            return json.loads(resp.text)
        get_url = resp.headers["operation-location"]
    except Exception as e:
        return json.loads(('{"error":{"code":"POSTUnkownError", "message":"'+str(e)+'"}}'))
    print("post_success")
    n_tries = 10
    n_try = 0
    wait_sec = 6
    while n_try < n_tries:
        try:
            resp = get(url = get_url, headers = {"Ocp-Apim-Subscription-Key": apim_key})
            resp_json = json.loads(resp.text)
            if resp.status_code != 200:
                return resp_json
            status = resp_json["status"]
            if status == "succeeded":
                return resp_json
            if status == "failed":
                return json.loads('{"error":{"code":"AnalysisFailed", "message":"Can\'t analyze"}}')
            # Analysis still running. Wait and retry.
            time.sleep(wait_sec)
            n_try += 1
        except Exception as e:
            return json.loads(('{"error":{"code":"GETUnkownError", "message":"' + str(e) + '"}}'))
    return json.loads(('{"error":{"code":"GETTimeLimitExceeded", "message":"may try later"}}'))

'''
r = form_recognizer_layout(
    r"C:\Users\Administrator\Desktop\OCR\OCR_doc\sample_data\Test\Invoice_6.pdf",
    'image/jpeg'
    )
'''