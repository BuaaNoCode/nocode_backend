########### Python Form Recognizer Async Layout #############
import json
import time
from requests import get, post


def form_recognizer_layout(source, files, content_type):
    # Endpoint URL
    endpoint = r" https://nocode-form-2.cognitiveservices.azure.com"
    apim_key = "d7596252a6f94d778db5897122013465"
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
        resp = post(url=post_url, data=data_bytes, headers=headers)
        if resp.status_code != 202:
            return json.loads(resp.text)
        get_url = resp.headers["operation-location"]
    except Exception as e:
        return json.loads(('{"error":{"code":"POSTUnkownError", "message":"'+str(e)+'"}}'))
    n_tries = 10
    n_try = 0
    wait_sec = 6
    while n_try < n_tries:
        try:
            resp = get(url=get_url, headers={"Ocp-Apim-Subscription-Key": apim_key})
            resp_json = json.loads(resp.text)
            if resp.status_code != 200:
                return resp_json
            status = resp_json["status"]
            if status == "succeeded":
                return resp_json
            if status == "failed":
                return {"error": {"code": "AnalysisFailed", "message": "Can\'t analyze"}}
            # Analysis still running. Wait and retry.
            time.sleep(wait_sec)
            n_try += 1
        except Exception as e:
            return {"error": {"code": "GetUnknownError", "message": str(e)}}
    return {"error": {"code": "GetTimeLimitExceeded", "message": "may try later"}}


def distEclud(a, b):
    return abs(a - b)


def K_Means(arr):
    K = 2
    p = []
    arr.sort()
    N = len(arr) - 1
    for i in range(0, N):
        p.append(arr[i + 1] - arr[i])
    p.sort()
    cluster = [p[0], p[N - 1]]
    pos = [1 for i in range(0, N)]
    for t in range(1, 101):
        for i in range(0, N):
            pos[i] = 0
            for j in range(1, K):
                if distEclud(cluster[pos[i]], p[i]) > distEclud(cluster[j], p[i]):
                    pos[i] = j
        num = [0 for i in range(0, K)]
        cluster = [0 for i in range(0, K)]
        for i in range(0, N):
            num[pos[i]] += 1
            cluster[pos[i]] += p[i]
        for i in range(0, K):
            cluster[i] /= num[i]
    eps = 0
    for i in range(N):
        if pos[i] == pos[0]:
            eps = max(eps, p[i])
    cnt = 0
    dic = {}
    lastVal = -2147483647
    for i in range(N + 1):
        if arr[i] - lastVal > eps:
            cnt = cnt + 1
        dic[arr[i]] = cnt
        lastVal = arr[i]
    dic["size"] = cnt
    return dic


def form_layout_analyze(r):
    sheets = r["analyzeResult"]["pageResults"][0]["tables"]
    if len(sheets) > 0:
        sheet = r["analyzeResult"]["pageResults"][0]["tables"][0]
        row = sheet["rows"]
        line = sheet["columns"]
        lastRow = 1
        for cell in sheet["cells"]:
            lastRow = cell["rowIndex"]
    else:
        infos = r["analyzeResult"]["readResults"][0]["lines"]
        arrx = []
        arry = []
        for info in infos:
            arrx.append(info["boundingBox"][0])
            arry.append(info["boundingBox"][1])
        dicx = K_Means(arrx)
        dicy = K_Means(arry)
        sheet = [[""] * dicx["size"] for i in range(dicy["size"])]
        for info in infos:
            sheet[dicy[info["boundingBox"][1]] - 1][dicx[info["boundingBox"][0]] - 1] = info["text"]
    return sheet
