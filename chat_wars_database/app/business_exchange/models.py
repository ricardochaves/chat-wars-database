from django.contrib.postgres.indexes import BrinIndex
from django.db import models

from chat_wars_database.app.business_core.models import Item


class ExchangeMessages(models.Model):

    message_id = models.IntegerField(unique=True)
    message_date = models.DateTimeField()
    message_text = models.TextField()

    class Meta:
        indexes = (BrinIndex(fields=["message_date"]), BrinIndex(fields=["message_id"]))


class StatsByDay(models.Model):

    date = models.DateField()
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    units = models.IntegerField()
    average_value = models.DecimalField(max_digits=8, decimal_places=2)
    mean_value = models.IntegerField()
    min_value = models.IntegerField()
    max_value = models.IntegerField()

    min_value_message_id = models.IntegerField(default=0)
    max_value_message_id = models.IntegerField(default=0)

    deerhorn_castle_seller = models.IntegerField(default=0)
    dragonscale_castle_seller = models.IntegerField(default=0)
    highnest_castle_seller = models.IntegerField(default=0)
    moonlight_castle_seller = models.IntegerField(default=0)
    potato_castle_seller = models.IntegerField(default=0)
    sharkteeth_castle_seller = models.IntegerField(default=0)
    wolfpack_castle_seller = models.IntegerField(default=0)

    deerhorn_castle_buyer = models.IntegerField(default=0)
    dragonscale_castle_buyer = models.IntegerField(default=0)
    highnest_castle_buyer = models.IntegerField(default=0)
    moonlight_castle_buyer = models.IntegerField(default=0)
    potato_castle_buyer = models.IntegerField(default=0)
    sharkteeth_castle_buyer = models.IntegerField(default=0)
    wolfpack_castle_buyer = models.IntegerField(default=0)
