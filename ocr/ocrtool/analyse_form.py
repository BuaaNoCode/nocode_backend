########### Python Form Recognizer Async Analyze #############
import json
import time
from requests import get, post

def analyse_form(source,model_id,file_type):
# Endpoint URL
    endpoint = r"https://nocode-form-2.cognitiveservices.azure.com/"
    apim_key = "d7596252a6f94d778db5897122013465"
    model_id = model_id
    post_url = endpoint + "/formrecognizer/v2.0-preview/custom/models/%s/analyze" % model_id
    source = source
    params = {
        "includeTextDetails": True
    }

    headers = {
        # Request headers
        'Content-Type': file_type,
        'Ocp-Apim-Subscription-Key': apim_key,
    }
    with open(source, "rb") as f:
        data_bytes = f.read()

    try:
        resp = post(url = post_url, data = data_bytes, headers = headers, params = params)
        if resp.status_code != 202:
            quit()
        get_url = resp.headers["operation-location"]
    except Exception as e:
        quit()
    n_tries = 15
    n_try = 0
    wait_sec = 5
    max_wait_sec = 60
    while n_try < n_tries:
        try:
            resp = get(url = get_url, headers = {"Ocp-Apim-Subscription-Key": apim_key})
            resp_json = resp.json()
            if resp.status_code != 200:
                quit()
            status = resp_json["status"]
            if status == "succeeded":
                return resp_json
                quit()
            if status == "failed":
                quit()
            # Analysis still running. Wait and retry.
            time.sleep(wait_sec)
            n_try += 1
            wait_sec = min(2*wait_sec, max_wait_sec)
        except Exception as e:
            msg = "GET analyze results failed:\n%s" % str(e)
            quit()
    print("Analyze operation did not complete within the allocated time.")