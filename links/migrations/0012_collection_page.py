# Generated by Django 2.2.7 on 2019-12-02 16:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0011_page'),
    ]

    operations = [
        migrations.AddField(
            model_name='collection',
            name='page',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='links.Page'),
        ),
    ]
