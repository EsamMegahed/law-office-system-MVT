# Generated by Django 5.0.7 on 2024-09-09 15:49

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ActiveLawyer',
            new_name='LawyerActive',
        ),
    ]
