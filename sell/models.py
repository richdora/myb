from django.db import models
from photo.utils import compress_image, create_thumbnail
from django.conf import settings

from django.utils import timezone

class SellItem(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    photo1 = models.ImageField(upload_to='sell_items/', null=True, blank=True)
    photo2 = models.ImageField(upload_to='sell_items/', null=True, blank=True)
    photo3 = models.ImageField(upload_to='sell_items/', null=True, blank=True)
    photo1_thumbnail = models.ImageField(upload_to='thumbnails/', null=True, blank=True)
    photo2_thumbnail = models.ImageField(upload_to='thumbnails/', null=True, blank=True)
    photo3_thumbnail = models.ImageField(upload_to='thumbnails/', null=True, blank=True)

    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Compress and create thumbnails for each photo
        if self.photo1:
            compress_image(self.photo1)
            self.photo1_thumbnail = create_thumbnail(self.photo1)

        if self.photo2:
            compress_image(self.photo2)
            self.photo2_thumbnail = create_thumbnail(self.photo2)

        if self.photo3:
            compress_image(self.photo3)
            self.photo3_thumbnail = create_thumbnail(self.photo3)

        super().save(update_fields=['photo1_thumbnail', 'photo2_thumbnail', 'photo3_thumbnail'])
