from django.db import models



class Post(models.Model):
    """Database model for tracking events"""

    rare_user = models.ForeignKey("RareUser", on_delete=models.CASCADE, related_name="posts")
    category = models.ForeignKey("Category", on_delete=models.CASCADE, related_name="posts" )
    title = models.CharField(max_length=200)
    publication_date = models.DateField(auto_now_add=True)
    image_url = models.URLField()
    content = models.CharField(max_length=200)
    approved = models.BooleanField()
    tags = models.ManyToManyField("Tag", through="PostTag", related_name="posts")