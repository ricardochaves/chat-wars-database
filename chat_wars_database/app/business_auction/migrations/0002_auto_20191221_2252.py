# Generated by Django 3.0.1 on 2019-12-21 22:52

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [("business_auction", "0001_initial")]

    operations = [
        migrations.AlterField(
            model_name="auctionlotbids", name="buyer_name", field=models.CharField(blank=True, max_length=50, null=True)
        )
    ]
