# Generated by Django 4.2 on 2023-05-31 01:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photo', '0003_photo_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='secrets',
            field=models.TextField(blank=True),
        ),
    ]
