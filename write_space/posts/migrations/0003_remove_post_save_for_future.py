# Generated by Django 2.1.5 on 2019-05-03 22:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_auto_20190503_0238'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='save_for_future',
        ),
    ]
