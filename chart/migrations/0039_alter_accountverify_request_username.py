# Generated by Django 4.1.2 on 2022-12-10 13:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chart', '0038_rename_username_accountverify_request_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountverify',
            name='request_username',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='req_user', to=settings.AUTH_USER_MODEL),
        ),
    ]