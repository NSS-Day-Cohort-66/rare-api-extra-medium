from django.db import models
from django.contrib.auth.models import User

class RareUser(models.Model):
    """Database model for tracking events"""

    bio = models.CharField(max_length=200)
    profile_image_url = models.URLField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rare_users")