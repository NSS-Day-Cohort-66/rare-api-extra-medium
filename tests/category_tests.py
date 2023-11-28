import json
from rest_framework import status
from rest_framework.test import APITestCase
from rareapi.models import RareUser, Category
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class CategoryTests(APITestCase):

    fixtures = ['user', 'token', 'rare_user','category']

    def setUp(self):
        # Assuming you have a user with ID 1 for testing purposes
        self.user = User.objects.first()
        self.rare_user = RareUser.objects.get(user=self.user)
       
        token= Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_create_category(self):
        """
        Ensure we can create a new category.
        """
        url = "/rareapi/categories/"

        data = {
            "label": "Wise"
        }

        response = self.client.post(url, data, format='json')

        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    # Assert that the properties on the created resource are correct
    
        self.assertEqual(json_response["label"], "Wise")
