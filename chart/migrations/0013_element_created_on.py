# Generated by Django 4.1.2 on 2022-11-12 16:34

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('chart', '0012_alter_profile_bio'),
    ]

    operations = [
        migrations.AddField(
            model_name='element',
            name='created_on',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined'),
        ),
    ]
