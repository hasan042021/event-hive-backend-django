# Generated by Django 5.1 on 2024-12-10 10:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0002_userprofile_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='image',
        ),
    ]
