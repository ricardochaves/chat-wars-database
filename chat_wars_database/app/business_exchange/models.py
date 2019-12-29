from django.contrib.postgres.indexes import BrinIndex
from django.db import models


class ExchangeMessages(models.Model):

    message_id = models.IntegerField(unique=True)
    message_date = models.DateTimeField()
    message_text = models.TextField()

    class Meta:
        indexes = (BrinIndex(fields=["message_date"]), BrinIndex(fields=["message_id"]))
