# Generated by Django 4.2 on 2023-04-29 01:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SellItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('comment', models.TextField(blank=True, null=True)),
                ('photo1', models.ImageField(blank=True, null=True, upload_to='sell_items/')),
                ('photo2', models.ImageField(blank=True, null=True, upload_to='sell_items/')),
                ('photo3', models.ImageField(blank=True, null=True, upload_to='sell_items/')),
                ('photo1_thumbnail', models.ImageField(blank=True, null=True, upload_to='thumbnails/')),
                ('photo2_thumbnail', models.ImageField(blank=True, null=True, upload_to='thumbnails/')),
                ('photo3_thumbnail', models.ImageField(blank=True, null=True, upload_to='thumbnails/')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
