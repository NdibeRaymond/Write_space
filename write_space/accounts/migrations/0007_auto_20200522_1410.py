# Generated by Django 2.2.2 on 2020-05-22 13:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20200522_0417'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='_background_pic',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='_profile_pic',
        ),
    ]
