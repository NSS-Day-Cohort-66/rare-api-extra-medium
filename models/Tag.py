from django.db import models


class Tag(models.Model):
    """Database model for tracking events"""

    
    label = models.CharField(max_length=200)
    