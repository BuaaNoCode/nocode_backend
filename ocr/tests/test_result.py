from django.test import TestCase
from django.contrib.auth import get_user_model
from django.test import Client
import json
import os
from ocr.models.project import Project
from ocr.models.recognition_result import RecognitionResult

class ProjectTestCase(TestCase):
    def setUp(self):
        self.c = Client()
        self.UserModel = get_user_model()

    def test_receieve_ocr_photo(self):
        self.c.post('/auth/create', {'username':'testuser2', 'password':'password', 'email':'email'}, {'content_type':"application/json"})
        response = self.c.post('/auth/', {'username':'testuser2', 'password':'password'}, {'content_type':"application/json"})
        access_token = json.loads(response.content.decode())['access_token']
        self.c.defaults['HTTP_AUTHORIZATION'] = 'Bearer ' + access_token
        self.c.post('/ocr/project', {'name': 'project1', 'comment': 'comment1'},
                    {'content_type':"application/json"})
        data = json.loads(response.content.decode())
        project_id = data['id']
        project = Project.objects.filter(id=project_id)

        file = 'form.png'
        payload = {'name': 'result1', 'comment': 'resultcomment1'}
        files = {
            "json": (None, json.dumps(payload), "application/json"),
            "file": (os.path.basename(file), open(file, "rb"), "image/png")
        }
        response = self.c.post('/ocr/project/'+project_id, files=files)
        data = json.loads(response.content.decode())
        result = project.recognitionresult_set.filter(id=data['id'])
        self.assertEqual(result.name, 'result1')
        self.assertEqual(result.comment, 'resultcomment1')

    def test_retrieve_ocr_result(self):
        project = Project.objects.filter(belong_to=self.c).first()
        result = project.recognitionresult_set.all().first()
        response = self.c.get('/ocr/project/'+project.id+'/'+result.id, {}, {'content_type': "application/json"})
        data = json.loads(response.content.decode())
        self.assertEqual(data['id'], result.id)
        self.assertEqual(data['name'], result.name)
        self.assertEqual(data['comment'], result.comment)
        self.assertEqual(data['result'], result.result)

    def test_update_ocr_result(self):
        project = Project.objects.filter(belong_to=self.c).first()
        result = project.recognitionresult_set.all().first()
        self.c.put('/ocr/project/'+project.id+'/'+result.id, {'name': 'result2', 'comment': 'resultcomment2'},
                   {'content_type': "application/json"})
        result = RecognitionResult.objects.filter(id=result.id)
        self.assertEqual(result.name, 'result2')
        self.assertEqual(result.comment, 'resultcomment2')

    def test_remove_ocr_result(self):
        project = Project.objects.filter(belong_to=self.c).first()
        result = project.recognitionresult_set.all().first()
        self.c.delete('/ocr/project/'+project.id+'/'+result.id, {}, {'content_type': "application/json"})
        self.assertEqual(RecognitionResult.objects.count(), 0)