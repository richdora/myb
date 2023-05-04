from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

class Movie(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    youtube_link = models.URLField()
    comments = models.TextField(blank=True, null=True)  # Add this line
    title = models.CharField(max_length=200)
    url = models.URLField()

    def __str__(self):
        return self.title
