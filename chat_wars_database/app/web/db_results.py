from typing import List
from typing import Optional

from django.db.models import Avg
from django.db.models.functions import TruncDate

from chat_wars_database.app.business_auction.models import AuctionLot
from chat_wars_database.app.business_core.models import Item


def get_more_expensive_lot() -> AuctionLot:

    return AuctionLot.objects.order_by("-price").first()


def get_first_lot_in_db() -> AuctionLot:

    return AuctionLot.objects.order_by("lot_id").first()


def get_total_active_lots() -> int:
    return AuctionLot.objects.filter(status=1).count()


def get_all_items() -> List[Item]:
    return Item.objects.filter(command__isnull=False).all()


def get_items_from_command(command: str) -> List[AuctionLot]:

    return AuctionLot.objects.filter(item__command=command).order_by("message_date").all()


def get_item_from_command(command: str) -> Optional[Item]:

    return Item.objects.filter(command=command).first()


def get_auctions_average(command: str) -> List:

    return (
        AuctionLot.objects.filter(item__command=command)
        .annotate(d=TruncDate("message_date"))
        .values("d")
        .annotate(Avg("price"))
    )


def get_first_lot(command: str) -> AuctionLot:
    return AuctionLot.objects.filter(item__command=command).order_by("message_date").first()


def get_last_lot(command: str) -> AuctionLot:
    return AuctionLot.objects.filter(item__command=command).order_by("-message_date").first()


def get_cheaper_lot(command: str) -> AuctionLot:
    return AuctionLot.objects.filter(item__command=command).order_by("price").first()


def get_more_expensive(command: str) -> AuctionLot:
    return AuctionLot.objects.filter(item__command=command).order_by("-price").first()
