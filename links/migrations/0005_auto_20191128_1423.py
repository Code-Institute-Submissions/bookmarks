# Generated by Django 2.2.7 on 2019-11-28 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0004_bookmark_collection'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookmark',
            name='url',
            field=models.URLField(),
        ),
    ]
