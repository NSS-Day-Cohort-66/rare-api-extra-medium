import json
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User


class AuthTests(APITestCase):

    fixtures = [ 'user', 'token']

    def setUp(self):
        self.user = User.objects.first()
        self.token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        print(self.user)
        print(self.token)

    def test_login_valid_user(self):
        
        data = {
            "username": "meg@ducharme.com",
            "password": "ducharme"
        }

        print(data)

        response = self.client.post("/login", data, format='json')
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(json_response["token"], "1600073627c3344754172dd997452440b1ddba7a")

    def test_register_user(self):
        
        data = {
            "username": "new_user",
            "password": "new_user",
            "first_name": "new",
            "last_name": "user",
            "email": "new@user.com",
            "bio": "I am a new user",
            "profile_image_url": "http://example.com",
            "active": True,
        }


        response = self.client.post("/register", data, format='json')
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertIsNotNone(json_response["token"])


        
