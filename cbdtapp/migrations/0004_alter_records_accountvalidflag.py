# Generated by Django 3.2.12 on 2022-03-17 05:07

from django.db import migrations, models
import django_cryptography.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cbdtapp', '0003_auto_20220317_1021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='records',
            name='accountValidFlag',
            field=django_cryptography.fields.encrypt(models.CharField(max_length=2)),
        ),
    ]
