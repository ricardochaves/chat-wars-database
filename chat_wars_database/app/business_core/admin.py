from django.contrib import admin

from chat_wars_database.app.business_core.models import Item


@admin.register(Item)
class AuctionLotAdmin(admin.ModelAdmin):
    list_display = ("command", "name")
    # list_filter = ("message_date",)
    # ordering = ["-lot_id"]
