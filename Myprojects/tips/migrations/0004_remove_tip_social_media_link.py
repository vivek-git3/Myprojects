# Generated by Django 5.1.1 on 2024-10-13 15:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tips', '0003_tip_social_media_link'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tip',
            name='social_media_link',
        ),
    ]
