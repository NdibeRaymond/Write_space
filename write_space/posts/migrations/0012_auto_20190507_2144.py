# Generated by Django 2.1.5 on 2019-05-07 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0011_auto_20190507_2140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_heading',
            field=models.CharField(max_length=120),
        ),
    ]
