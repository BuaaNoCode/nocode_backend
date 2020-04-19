from django.shortcuts import render
from django.http import HttpResponse, QueryDict
import json
from django.views.decorators.csrf import csrf_exempt
from ocr.models.project import Project
from ocr.models.recognition_result import RecognitionResult
from django.utils import timezone


def generalPro(request):
    if request.method == 'POST':
    """create a project

    [route]: /ocr/project

    [method]: POST

    [Request Body]: 
        name string
        comment string
    
    [Response Body]:
        id integer
        created_at datetime
    """
        print('Post success')
        concat = request.POST
        postBody = request.postBody
        print(concat)
        print(postBody)
        json_result = json.loads(postBody)
        print(json_result)
        
        pname = json_result['name']
        pcomment = json_result['comment']
        pcreated_at = timezone.now()
        newProject = Project(name=pname, comment=pcomment, created_at=pcreated_at)
        newProject.save()

        return JsonResponse({'id' : newProject.id, 'created_at' : pcreated_at})

    else if request.method == 'GET':
    """get information of all projects

    [route]: /ocr/project

    [method]: GET

    [Response Body]: 
        projects array
        project_num integer
    """
        return JsonResponse({'projects':Project.objects.all(), 'project_num':Project.objects.count()})

    else:
        return HttpResponse('方法错误')

def detailPro(request, p1):
    if request.method == 'PUT':
    """modify specific project

    [route]: /ocr/project/<int:project_id>

    [method]: PUT

    [Request Body]: 
        name string
        comment string
    """
        put = QueryDict(request.body)
        pname = put.get('name')
        pcomment = put.get('comment')

        p = Project.objects.get(id=p1)
        p.name = pname
        p.comment = pcomment
        p.save()

    else if request.method == 'GET':
    """get information of specific project

    [route]: /ocr/project/<int:project_id>

    [method]: GET

    [Response Body]: 
        name string
        comment string
        created_at datetime
        result_num integer
        results array
    """
        p = Project.objects.get(id=p1)
        name = p.name
        comment = p.comment
        created_at = p.created_at
        result_num = p.recognitionResult_set.count()
        results = p.recognitionResult_set.all()
        data = {'name':name, 'comment':comment, 'created_at':created_at, 'result_num':result_num, 'results':results}
        return JsonResponse(data)

    else if request.method == 'DELETE':
     """delete specific project

    [route]: /ocr/project/<int:project_id>

    [method]: DELETE
    """
        p = Project.objects.get(id=p1)
        p.delete()

    else if request.method == 'POST':
    """upload image

    [route]: /ocr/project/<int:project_id>

    [method]: GET

    [Request Body]: 
        name string (optional, recognition result)
        comment string (optional, recognition result)

    [Response Body]: 
        id integer
        created_at datetime
    """
        json_text = request.FILES.get("json", None)
        json_result = json.loads(json_text)
        print(json_result)      
        rname = json_result['name']
        rcomment = json_result['comment']
        
        image = request.FILES.get("file", None)    # png  
        if not image:  
            returnHttpResponse("no images for upload!")
        
        p = Project.objects.get(id=p1)
        r = p.recognitionResult_set.create(name=rname, comment=rcomment, created_at=timezone.now())
        result = handle_ocr()
        r.result = result 
        r.save()

        data = {"id":r.id, "created_at":r.created_at}
        return JsonResponse(data)

    else:
        return HttpResponse('方法错误')

def result(request, p1, p2):
    if request.method == 'GET':
    """return recognition result

    [route]: /ocr/project/<int:project_id>/<int:result_id>

    [method]: GET

    [Response Body]: 
        name string
        comment string
        result json
    """
        p = Project.objects.get(id=p1)
        r = p.recognitionResult_set.filter(id=p2)
        data = {"name":r.name, "comment":r.comment, "result":r.result}
        return JsonResponse(data)

    else if request.method == 'PUT':
    """modify recognition result

    [route]: /ocr/project/<int:project_id>/<int:result_id>

    [method]: PUT

    [Request Body]: 
        name string
        comment string
    """
        p = Project.objects.get(id=p1)
        r = p.recognitionResult_set.filter(id=p2)
        put = QueryDict(request.body)
        rname = put.get('name')
        rcomment = put.get('comment')
        r.name = rname
        r.comment = rcomment

    else if request.method == 'DELETE':
    """delete recognition result

    [route]: /ocr/project/<int:project_id>/<int:result_id>

    [method]: DELETE
    """
        p = Project.objects.get(id=p1)
        r = p.recognitionResult_set.filter(id=p2)
        r.delete()

    else:
        return HttpResponse('方法错误')




def handle_ocr():
    # ocr对接