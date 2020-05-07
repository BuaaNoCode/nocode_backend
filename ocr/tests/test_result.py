import json
import os

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.test import Client, TestCase

from common.consts import VIP
from ocr.models.project import Project
from ocr.models.recognition_result import RecognitionResult


class ResultTestCase(TestCase):
    def setUp(self):
        self.c = Client()
        self.UserModel = get_user_model()
        self.c.post('/auth/create', {'username': 'testuser', 'password': 'password', 'email': 'email'},
                    content_type="application/json")
        response = self.c.post('/auth/', {'username': 'testuser', 'password': 'password'},
                               content_type="application/json")
        access_token = json.loads(response.content.decode())['access_token']
        self.c.defaults['HTTP_AUTHORIZATION'] = 'Bearer ' + access_token
        self.user = User.objects.get(username='testuser')

        # create project
        self.c.post('/ocr/project', {'name': 'project1', 'comment': 'comment1'},
                    content_type="application/json")
        project = Project.objects.first()
        # create result
        RecognitionResult.objects.create(**{
            "name": "test result",
            "comment": "test comment",
            "belong_to": project,
            "result": {}
        })

        # set files
        # file = './ocr/tests/form.png'
        # payload = {'name': 'result1', 'comment': 'resultcomment1'}
        # self.files = {
        #     "json": json.dumps(payload),
        #     "file": (os.path.basename(file), open(file, "rb"), "image/png")
        # }

    # def test_receive_ocr_photo(self):
    #     project = Project.objects.first()
    #     response = self.c.post('/ocr/project/' + str(project.id), self.files)
    #     data = json.loads(response.content.decode())
    #     result = project.recognitionresult_set.get(id=data.get('id'))
    #     self.assertEqual(result.name, 'result1')
    #     self.assertEqual(result.comment, 'resultcomment1')

    def test_retrieve_ocr_result(self):
        # upload photo
        project = Project.objects.first()
        # self.c.post('/ocr/project/' + str(project.id), self.files)

        result = project.recognitionresult_set.first()
        response = self.c.get('/ocr/project/'+str(project.id)+'/'+str(result.id), {}, content_type="application/json")
        data = json.loads(response.content.decode())

        self.assertEqual(data['id'], result.id)
        self.assertEqual(data['name'], result.name)
        self.assertEqual(data['comment'], result.comment)
        self.assertEqual(data['result'], result.result)

    def test_update_ocr_result(self):
        # upload photo
        project = Project.objects.first()
        # self.c.post('/ocr/project/' + str(project.id), self.files)

        result = project.recognitionresult_set.all().first()
        self.c.put('/ocr/project/'+str(project.id)+'/'+str(result.id), {'name': 'result2', 'comment': 'resultcomment2'},
                   content_type="application/json")
        result = RecognitionResult.objects.get(belong_to=project, id=result.id)
        self.assertEqual(result.name, 'result2')
        self.assertEqual(result.comment, 'resultcomment2')

    def test_remove_ocr_result(self):
        # upload photo
        project = Project.objects.first()
        # self.c.post('/ocr/project/' + str(project.id), self.files)

        result = project.recognitionresult_set.all().first()
        self.assertEqual(RecognitionResult.objects.count(), 1)
        self.c.delete('/ocr/project/'+str(project.id)+'/'+str(result.id), {}, content_type="application/json")
        self.assertEqual(RecognitionResult.objects.count(), 0)
