# Generated by Django 2.1.5 on 2019-05-04 01:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_userprofile_saved_for_future'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='following',
            field=models.ManyToManyField(to='accounts.userProfile'),
        ),
    ]
