# Generated by Django 4.2 on 2023-05-30 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('memo', '0003_tag_memo_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='memo',
            name='password',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]
