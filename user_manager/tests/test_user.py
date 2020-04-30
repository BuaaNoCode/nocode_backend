from django.test import TestCase
from django.contrib.auth import get_user_model
from django.test import Client
import json

class UserTest(TestCase):
    def setUp(self):
        self.c = Client()
        self.UserModel = get_user_model()

    def test_create_user(self):
        self.c.post('/auth/create', {'username':'testuser1', 'password':'password', 'email':'email'}, content_type="application/json")
        response = self.c.post('/auth/', {'username':'testuser1', 'password':'password'}, content_type="application/json")
        data = json.loads(response.content.decode())
        self.assertTrue('access_token' in data)


    def test_disable_user(self):
        self.c.post('/auth/create', {'username':'testuser2', 'password':'password', 'email':'email'}, content_type="application/json")

        logged_in = self.c.post('/auth/', {'username':'testuser2', 'password':'password'}, content_type="application/json")
        access_token = json.loads(logged_in.content.decode())['access_token']
        self.c.defaults['HTTP_AUTHORIZATION'] = 'Bearer ' + access_token

        self.c.post('/auth/disable', {'username':'testuser2', 'password':'password'}, content_type="application/json")

        response = self.c.post('/auth/', {'username':'testuser2', 'password':'password'}, content_type="application/json")
        data = json.loads(response.content.decode())
        self.assertTrue(data['code'] == 401)


    def test_reset_user_password(self):
        self.c.post('/auth/create', {'username':'testuser3', 'password':'password', 'email':'email'}, content_type="application/json")

        logged_in = self.c.post('/auth/', {'username':'testuser3', 'password':'password'}, content_type="application/json")
        access_token = json.loads(logged_in.content.decode())['access_token']
        self.c.defaults['HTTP_AUTHORIZATION'] = 'Bearer ' + access_token

        self.c.post('/auth/reset', {'username':'testuser3', 'password':'password', 'new_password':'new_password'}, content_type="application/json")
        self.assertTrue(self.UserModel.objects.get(username='testuser3').check_password('new_password'))