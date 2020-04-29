import http.client, urllib.request, urllib.parse, urllib.error, base64

def form_recognizer():
    apim_key = "d7596252a6f94d778db5897122013465"
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': apim_key,
    }

    params = urllib.parse.urlencode({
        # Request parameters
        'includeTextDetails': '{boolean}',
    })

    try:
        print("1\n")
        conn = http.client.HTTPSConnection('westus2.api.cognitive.microsoft.com')
        conn.request("POST", "/formrecognizer/v2.0-preview/custom/models/{modelId}/analyze?%s" % params, "{body}",
                     headers)
        '''调用时这里需要修改，model id'''
        print("2\n")
        response = conn.getresponse()
        print("3\n")
        data = response.read()
        print("4\n")
        print(data)
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

def get_analyze_form_result():
    apim_key = "d7596252a6f94d778db5897122013465"
    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': apim_key,
    }

    params = urllib.parse.urlencode({
    })

    try:
        conn = http.client.HTTPSConnection('westus2.api.cognitive.microsoft.com')
        conn.request("GET",
                     "/formrecognizer/v2.0-preview/custom/models/{modelId}/analyzeResults/{resultId}?%s" % params,
                     "{body}", headers)
        '''修改网址为相应路径'''
        response = conn.getresponse()
        data = response.read()
        print(data)
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

r = form_recognizer()
print("5\n")
print(r)
get_analyze_form_result()
exit(0)

