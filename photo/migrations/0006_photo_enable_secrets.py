# Generated by Django 4.2 on 2023-06-03 03:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photo', '0005_photo_range'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='enable_secrets',
            field=models.BooleanField(default=False),
        ),
    ]
