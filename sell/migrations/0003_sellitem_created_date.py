# Generated by Django 4.2 on 2023-04-24 07:47

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('sell', '0002_sellitem_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='sellitem',
            name='created_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
