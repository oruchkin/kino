# Generated by Django 4.0 on 2022-08-08 18:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='person_filmwork',
            old_name='role',
            new_name='sandwich',
        ),
    ]
