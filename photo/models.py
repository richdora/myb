from django.db import models
from django.conf import settings
from photo.utils import compress_image, create_thumbnail


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Photo(models.Model):
    image = models.ImageField(upload_to='photos/')
    comment = models.TextField(blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    thumbnail = models.ImageField(upload_to='thumbnails/', null=True, blank=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return f'{self.user.username} - {self.comment[:20]}'

