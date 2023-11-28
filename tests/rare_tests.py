import json
from rest_framework import status
from rest_framework.test import APITestCase
from rareapi.models import Category, Comment, Post, Tag, RareUser
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class RareAPITests(APITestCase):

    fixtures = ['categories', 'comments', 'posts', 'tags']

    def setUp(self):
        # Assuming you have a user with ID 1 for testing purposes
        self.user = User.objects.get(pk=2)
        #addess rareuser?
        token = Token.objects.get(user=self.user)
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
        self.assertEqual(json_response["label"], "Wise")

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

    def test_create_post(self):
        """
        Ensure we can create a new post.
        """
        url = "/rareapi/posts/"

        data = {
            "rare_user": 1,
            "category": 1,
            "title": "Post Title 1",
            "publication_date": "2023-01-01",
            "image_url": "https://example.com/image1.jpg",
            "content": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            "approved": True
        }

        response = self.client.post(url, data, format='json')

        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json_response["title"], "Post Title 1")

    def test_create_tag(self):
        """
        Ensure we can create a new tag.
        """
        url = "/rareapi/tags/"

        data = {
            "label": "Funny"
        }

        response = self.client.post(url, data, format='json')

        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json_response["label"], "Funny")

