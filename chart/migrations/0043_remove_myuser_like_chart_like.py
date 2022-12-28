# Generated by Django 4.1.2 on 2022-12-25 11:09

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chart', '0042_rename_likes_myuser_like'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myuser',
            name='like',
        ),
        migrations.AddField(
            model_name='chart',
            name='like',
            field=models.ManyToManyField(blank=True, related_name='like', to=settings.AUTH_USER_MODEL),
        ),
    ]