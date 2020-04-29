########### Python Form Recognizer Labeled Async Train #############

import json
import time
from requests import get, post
import requests
# Endpoint URL

def ocr_train(source,useLabelFile,content_type,prefix,includeSubFolders):
    endpoint = r"https://nocode-form-2.cognitiveservices.azure.com/"#Form Recognizer资源的端点URL。
    post_url = endpoint + r"/formrecognizer/v2.0-preview/custom/models"
    source = source #SAS URL为azure Blob存储容器的URL
    prefix = prefix #表单所在的Blob存储中的文件夹路径。根目录时候为空
    #prefix = "<Blob folder name>"#表单所在的Blob存储中的文件夹路径。根目录时候为空
    includeSubFolders = includeSubFolders
    useLabelFile = useLabelFile

    headers = {
        # Request headers
        'Content-Type': content_type,
        'Ocp-Apim-Subscription-Key': 'your key',#<subscription key>创建表单识别器资源时的订阅密钥。
    }

    body = 	{
        "source": source,
        "sourceFilter": {
            "prefix": prefix,
            "includeSubFolders": includeSubFolders
        },
        "useLabelFile": useLabelFile
    }

    try:
        resp = post(url = post_url, json = body, headers = headers)
        if resp.status_code != 201:
            print("POST model failed (%s):\n%s" % (resp.status_code, json.dumps(resp.json())))
            quit()
        print("POST model succeeded:\n%s" % resp.headers)
        get_url = resp.headers["location"]
    except Exception as e:
        print("POST model failed:\n%s" % str(e))
        quit()


    n_tries = 15
    n_try = 0
    wait_sec = 5
    max_wait_sec = 60
    while n_try < n_tries:
        try:
            resp = get(url = get_url, headers = headers)
            resp_json = resp.json()
            if resp.status_code != 200:
                print("GET model failed (%s):\n%s" % (resp.status_code, json.dumps(resp_json)))
                quit()
            model_status = resp_json["modelInfo"]["status"]#important message
            if model_status == "ready":
                print("Training succeeded:\n%s" % json.dumps(resp_json))
                return resp_json
                quit()
            if model_status == "invalid":
                print("Training failed. Model is invalid:\n%s" % json.dumps(resp_json))
                quit()
            # Training still running. Wait and retry.
            time.sleep(wait_sec)
            n_try += 1
            wait_sec = min(2*wait_sec, max_wait_sec)
        except Exception as e:
            msg = "GET model failed:\n%s" % str(e)
            print(msg)
            quit()
    print("Train operation did not complete within the allocated time.")

'''
r = ocr_train(
    source="https://nocode1.blob.core.windows.net/nocodeblob?sp=racwdl&st=2020-04-23T15:40:03Z&se=2020-06-24T15:40:00Z&sv=2019-02-02&sr=c&sig=JCIzp3zbYS9DP%2FavnBYLh5rqB0upg%2BO6SDmmmN3tZMU%3D",
    useLabelFile=False,
    content_type="application/pdf",
    prefix="",
    includeSubFolders=False
)
'''
#print(r)
#print('end_of_ocr_train')