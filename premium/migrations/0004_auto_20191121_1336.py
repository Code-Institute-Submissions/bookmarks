# Generated by Django 2.2.7 on 2019-11-21 13:36

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('premium', '0003_purchasepremium'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PurchasePremium',
            new_name='PremiumPurchase',
        ),
    ]
