# Generated by Django 5.1.1 on 2024-10-13 12:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tips', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tip',
            old_name='liked_by',
            new_name='likes',
        ),
    ]
