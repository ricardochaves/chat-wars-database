from django.db import models


class Item(models.Model):

    command = models.CharField(max_length=10, blank=True, null=True)
    name = models.CharField(max_length=200)
