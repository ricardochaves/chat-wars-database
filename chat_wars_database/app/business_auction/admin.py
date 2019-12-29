from django.contrib import admin

from chat_wars_database.app.business_auction.models import AuctionLot


@admin.register(AuctionLot)
class AuctionLotAdmin(admin.ModelAdmin):
    list_display = ("message_date", "lot_id", "auction_item", "price", "status")
    list_filter = ("message_date",)
    ordering = ["-lot_id"]
