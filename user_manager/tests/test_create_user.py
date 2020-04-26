from django.test import TestCase
from django.contrib.auth import get_user_model
from django.test import Client

class UserTest(TestCase):
    def setUp(self):
        self.c = Client()
        self.UserModel = get_user_model()

    def test_create_user(self):
        self.c.post('/auth/create', {'username':'testuser', 'password':'password', 'email':'email'})
        self.assertTrue(self.UserModel.objects.get(username='testuser') != None)

    def test_disable_user(self):
        self.c.post('/auth/create', {'username':'testuser', 'password':'password', 'email':'email'})
        self.c.post('/auth/disable', {'username':'testuser', 'password':'password'})
        self.assertRaises(Exception, self.UserModel.objects.get(username='testuser'))

    def test_reset_user_password(self):
        self.c.post('/auth/create', {'username':'testuser', 'password':'password', 'email':'email'})
        self.c.post('/auth/reset', {'username':'testuser', 'password':'password', 'new_password':'new_password'})
        self.assertTrue(self.UserModel.objects.get(username='testuser').check_password('password'))