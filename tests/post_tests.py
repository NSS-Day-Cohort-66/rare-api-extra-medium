import json
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rareapi.models import RareUser

class PostTests(APITestCase):
    
    fixtures = []
    
    def setUp(self):
        self.user = User.objects.first()
        self.rare_user = RareUser.objects.get(user=self.user)
       
        token= Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
        
        
   