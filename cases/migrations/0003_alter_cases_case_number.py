# Generated by Django 5.0.7 on 2024-09-14 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0002_alter_casepayment_cases_alter_casepayment_paid_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cases',
            name='case_number',
            field=models.CharField(max_length=300, verbose_name='case number'),
        ),
    ]
