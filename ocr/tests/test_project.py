from django.test import TestCase
from django.contrib.auth import get_user_model
from django.test import Client
import json
from ocr.models.project import Project
from ocr.models.recognition_result import RecognitionResult
from django.contrib.auth.models import User
from django.db.models import Count

class ProjectTestCase(TestCase):
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

    def test_create_project(self):
        response = self.c.post('/ocr/project', {'name': 'project1', 'comment': 'comment1'},
                    content_type="application/json")
        data = json.loads(response.content.decode())
        project_id = data.get("id")
        project = Project.objects.filter(id=project_id).first()
        self.assertEqual(project.name, 'project1')
        self.assertEqual(project.comment, 'comment1')

    def test_update_project(self):
        # create project
        self.c.post('/ocr/project', {'name': 'project1', 'comment': 'comment1'},
                    content_type="application/json")

        project_id = Project.objects.first().id
        self.c.put('/ocr/project/'+str(project_id), {'name': 'project2', 'comment': 'comment2'},
                    content_type="application/json")
        project = Project.objects.filter(id=project_id).first()
        self.assertEqual(project.name, 'project2')
        self.assertEqual(project.comment, 'comment2')

    def test_list_projects(self):
        # create project
        self.c.post('/ocr/project', {'name': 'project1', 'comment': 'comment1'},
                    content_type="application/json")

        response = self.c.get('/ocr/project', {}, content_type="application/json")
        data = json.loads(response.content.decode())
        project = Project.objects.get(belong_to=self.user)
        res = data.get('projects')[0]
        self.assertEqual(res['id'], project.id)
        self.assertEqual(res['name'], project.name)
        self.assertEqual(res['comment'], project.comment)
        self.assertEqual(res['results_num'], project.recognitionresult_set.count())
        self.assertEqual(data.get('project_num'), 1)

    def test_retrieve_project_detail(self):
        # create project
        self.c.post('/ocr/project', {'name': 'project1', 'comment': 'comment1'},
                    content_type="application/json")

        project = Project.objects.first()
        project.recognitionresult_set.create(name='testresult', comment='resultcomment', result ={})
        result = project.recognitionresult_set.first()

        response = self.c.get('/ocr/project/'+str(project.id), {}, content_type="application/json")
        data = json.loads(response.content.decode())

        self.assertEqual(data.get('name'), project.name)
        self.assertEqual(data.get('comment'), project.comment)
        self.assertEqual(data.get('result_num'), project.recognitionresult_set.count())
        res = data.get('results')[0]
        self.assertEqual(res['id'], result.id)
        self.assertEqual(res['name'], result.name)
        self.assertEqual(res['comment'], result.comment)

    def test_remove_project(self):
        # create project
        self.c.post('/ocr/project', {'name': 'project1', 'comment': 'comment1'},
                    content_type="application/json")
        self.assertEqual(Project.objects.count(), 1)

        project_id = Project.objects.first().id
        self.c.delete('/ocr/project/' + str(project_id), {}, content_type="application/json")
        self.assertEqual(Project.objects.count(), 0)