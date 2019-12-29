from django.contrib.postgres.indexes import BrinIndex
from django.db import models

from chat_wars_database.app.business_core.models import Item


class AuctionLot(models.Model):

    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    auction_item = models.CharField(max_length=200)
    message_id = models.IntegerField(unique=True)
    lot_id = models.IntegerField(unique=True)
    seller_name = models.CharField(max_length=50)
    seller_castle = models.CharField(max_length=30)
    started_price = models.IntegerField()
    message_date = models.DateTimeField()
    quality = models.IntegerField(null=True, blank=True)

    price = models.IntegerField()
    buyer_name = models.CharField(null=True, blank=True, max_length=50)
    buyer_castle = models.CharField(null=True, blank=True, max_length=30)
    status = models.IntegerField()

    end_at = models.CharField(max_length=50)
    real_time_end_at = models.DateTimeField()

    class Meta:
        indexes = (
            BrinIndex(fields=["lot_id"]),
            BrinIndex(fields=["message_date"]),
            BrinIndex(fields=["status"]),
            BrinIndex(fields=["message_id"]),
        )
