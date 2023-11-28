import json
from rest_framework import status
from rest_framework.test import APITestCase
from rareapi.models import RareUser
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class CommentTests(APITestCase):

    fixtures = ['user', 'token', 'rare_user','comment']

    def test_create_comment(self):
        """
        Ensure we can create a new comment.
        """
        url = "/rareapi/comments/"

        data = {
            "post": 1,
            "author": 1,
            "content": "This is a ROMAN post!",
            "created_on": "2023-11-16"
        }

        response = self.client.post(url, data, format='json')

        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        self.assertEqual(json_response["content"], "This is a ROMAN post!")