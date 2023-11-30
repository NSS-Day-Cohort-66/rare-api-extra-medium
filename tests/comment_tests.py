import json
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rareapi.models import RareUser


class CommentTests(APITestCase):
    fixtures = ["user", "rare_user", "token", "posts", "comments", "categories", "tags"]

    def setUp(self):
        self.user = User.objects.first()
        self.rare_user = RareUser.objects.get(user=self.user)
        token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_get_all_comments(self):
        response = self.client.get("/comments")

        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(json_response[0]["content"], "This is a great post!")
        self.assertEqual(json_response[1]["content"], "I enjoyed reading this.")
        self.assertEqual(json_response[2]["content"], "Interesting perspective.")
