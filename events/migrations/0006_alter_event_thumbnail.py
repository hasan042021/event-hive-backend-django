# Generated by Django 5.1 on 2024-12-13 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_rsvp_is_declined'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='thumbnail',
            field=models.URLField(blank=True, null=True),
        ),
    ]