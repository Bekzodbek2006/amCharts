# Generated by Django 4.1.2 on 2022-11-04 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chart', '0003_rename_descraption_chart_caption_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='heaven_to_heaven.png', upload_to='profile'),
        ),
    ]
