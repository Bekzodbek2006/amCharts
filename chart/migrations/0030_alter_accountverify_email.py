# Generated by Django 4.1.2 on 2022-12-05 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chart', '0029_remove_accountverify_verfy_account2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountverify',
            name='email',
            field=models.EmailField(max_length=254),
        ),
    ]