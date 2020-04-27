from django.test import TestCase
from django.contrib.auth import get_user_model
from django.test import Client
import json
from ocr.models.project import Project
from ocr.models.recognition_result import RecognitionResult

class ProjectTestCase(TestCase):
    def setUp(self):
        self.c = Client()
        self.UserModel = get_user_model()

    def test_create_project(self):
        self.c.post('/auth/create', {'username':'testuser', 'password':'password', 'email':'email'}, {'content_type':"application/json"})
        response = self.c.post('/auth/', {'username':'testuser', 'password':'password'}, {'content_type':"application/json"})
        access_token = json.loads(response.content.decode())['access_token']
        self.c.defaults['HTTP_AUTHORIZATION'] = 'Bearer ' + access_token

        self.c.post('/ocr/project', {'name': 'project1', 'comment': 'comment1'},
                    {'content_type':"application/json"})
        data = json.loads(response.content.decode())
        project_id = data['id']
        project = Project.objects.filter(id=project_id)
        self.assertEqual(project.name, 'project1')
        self.assertEqual(project.comment, 'comment1')

    def test_update_project(self):
        project_id = Project.objects.first().id
        self.c.put('/ocr/project/'+project_id, {'name': 'project2', 'comment': 'comment2'},
                    {'content_type': "application/json"})
        project = Project.objects.filter(id=project_id)
        self.assertEqual(project.name, 'project2')
        self.assertEqual(project.comment, 'comment2')

    def test_list_projects(self):
        response = self.c.get('/ocr/project', {}, {'content_type': "application/json"})
        data = json.loads(response.content.decode())
        projects = Project.objects.filter(belong_to=self.c)
        self.assertEqual(data['projects'], projects.values("id", "name", "comment", "created_at", "results_num"))
        self.assertEqual(data['project_num'], 1)

    def test_retrieve_project_detail(self):
        project_id = Project.objects.first().id
        response = self.c.get('/ocr/project/'+project_id, {}, {'content_type': "application/json"})
        data = json.loads(response.content.decode())
        project = Project.objects.first()
        result = RecognitionResult(name='testresult', comment='resultcomment', belong_to=project)
        result.save()
        results = result.belong_to.recognitionresult_set.all()

        self.assertEqual(data['name'], project.name)
        self.assertEqual(data['comment'], project.comment)
        self.assertEqual(data['created_at'], project.created_at)
        self.assertEqual(data['result_num'], project.recognitionresult_set.count())
        self.assertEqual(data['results'], results.values("id", "name", "comment", "created_at"))

    def test_remove_project(self):
        project_id = Project.objects.first().id
        self.c.delete('/ocr/project/' + project_id, {}, {'content_type': "application/json"})
        self.assertEqual(Project.objects.count(), 0)