# Generated by Django 4.2 on 2023-06-03 03:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photo', '0006_photo_enable_secrets'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='range',
            field=models.IntegerField(choices=[(50, '50m'), (100, '100m'), (1000, '1km'), (10000, '10km'), (100000, '100km')], default=50),
        ),
    ]
