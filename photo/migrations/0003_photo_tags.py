# Generated by Django 4.2 on 2023-05-07 22:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photo', '0002_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='tags',
            field=models.ManyToManyField(blank=True, to='photo.tag'),
        ),
    ]
