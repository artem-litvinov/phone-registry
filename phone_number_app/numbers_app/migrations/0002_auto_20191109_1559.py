# Generated by Django 2.2.7 on 2019-11-09 15:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('numbers_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='phonenumber',
            old_name='capasity',
            new_name='capacity',
        ),
    ]