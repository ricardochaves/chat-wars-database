# Generated by Django 3.0.1 on 2019-12-30 21:15

import django.db.models.deletion
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [("business_core", "0003_auto_20191230_2115"), ("business_exchange", "0001_initial")]

    operations = [
        migrations.CreateModel(
            name="StatsByDay",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("date", models.DateField()),
                ("units", models.IntegerField()),
                ("average_value", models.DecimalField(decimal_places=2, max_digits=8)),
                ("mean_value", models.IntegerField()),
                ("min_value", models.IntegerField()),
                ("max_value", models.IntegerField()),
                ("deerhorn_castle_seller", models.IntegerField(default=0)),
                ("dragonscale_castle_seller", models.IntegerField(default=0)),
                ("highnest_castle_seller", models.IntegerField(default=0)),
                ("moonlight_castle_seller", models.IntegerField(default=0)),
                ("potato_castle_seller", models.IntegerField(default=0)),
                ("sharkteeth_castle_seller", models.IntegerField(default=0)),
                ("wolfpack_castle_seller", models.IntegerField(default=0)),
                ("deerhorn_castle_buyer", models.IntegerField(default=0)),
                ("dragonscale_castle_buyer", models.IntegerField(default=0)),
                ("highnest_castle_buyer", models.IntegerField(default=0)),
                ("moonlight_castle_buyer", models.IntegerField(default=0)),
                ("potato_castle_buyer", models.IntegerField(default=0)),
                ("sharkteeth_castle_buyer", models.IntegerField(default=0)),
                ("wolfpack_castle_buyer", models.IntegerField(default=0)),
                ("item", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="business_core.Item")),
            ],
        )
    ]
