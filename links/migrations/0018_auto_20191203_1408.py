# Generated by Django 2.2.7 on 2019-12-03 14:08

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('links', '0017_auto_20191203_1407'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='page',
            unique_together={('position', 'user'), ('name', 'user')},
        ),
    ]
