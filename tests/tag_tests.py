import json
from rest_framework import status
from rest_framework.test import APITestCase
from rareapi.models import RareUser,Tag
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class TagTests(APITestCase):

    fixtures = ['user', 'token', 'rare_user','tag']
    
    def setUp(self):
        # Assuming you have a user with ID 1 for testing purposes
        self.user = User.objects.first()
        self.rare_user = RareUser.objects.get(user=self.user)
       
        token= Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
        
    def test_create_tag(self):
        """
        Ensure we can create a new tag.
        """
        url = "/rareapi/models/tags/"
        
        data = {
            "label": "Tagsss"
        }

        response = self.client.post(url, data, format='json')

        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json_response["label"], "Tagsss")

