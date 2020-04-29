from django.http import HttpResponse


def index(request):
    with open('nocode_backend/index.html') as file:
        html = file.read()
        print(html)

    return HttpResponse(html)