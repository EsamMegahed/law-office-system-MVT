# Generated by Django 5.0.7 on 2024-09-09 15:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_rename_activelawyer_lawyeractive'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lawyeractive',
            options={'permissions': (('Lawyer', 'lawyer'),)},
        ),
    ]
