# Generated by Django 3.2 on 2022-01-23 12:20

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20220112_0957'),
    ]

    operations = [
        migrations.AddField(
            model_name='worker',
            name='random_identifier',
            field=models.CharField(default='default.jpg', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='worker',
            name='worker_image',
            field=models.ImageField(default='default.jpg', upload_to=users.models.path_time),
        ),
    ]