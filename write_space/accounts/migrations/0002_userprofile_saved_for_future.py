# Generated by Django 2.1.5 on 2019-05-03 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_remove_post_save_for_future'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='saved_for_future',
            field=models.ManyToManyField(blank=True, related_name='saved', to='posts.Post'),
        ),
    ]