import datetime
import logging
import re
from typing import Dict
from typing import Optional
from typing import Tuple

from django.utils.timezone import make_aware

from chat_wars_database.app.business_auction.models import AuctionLot
from chat_wars_database.app.business_core.business import cleaner_item_name
from chat_wars_database.app.business_core.business import get_or_create_item

logger = logging.getLogger(__name__)


def create_lot(data: Dict) -> AuctionLot:

    # {
    #     "message": message,
    #     "message_id": event.message.id,
    #     "message_date": event.message.date,
    # }

    message = data["message"]
    message_id = data["message_id"]
    message_date = data["message_date"]

    lot_data = _build_data(message)

    lot = AuctionLot.objects.filter(lot_id=lot_data["lot_id"]).first()
    if lot:
        return lot

    item = get_or_create_item(lot_data["item"])

    return AuctionLot.objects.create(
        item=item,
        message_id=message_id,
        lot_id=lot_data["lot_id"],
        seller_name=lot_data["seller_name"],
        seller_castle=lot_data["seller_castle"],
        buyer_castle=lot_data["buyer_castle"],
        buyer_name=lot_data["buyer_name"],
        started_price=lot_data["price"],
        message_date=message_date,
        price=lot_data["price"],
        status=lot_data["status"],
        end_at=lot_data["end_at"],
        auction_item=lot_data["auction_item"],
        quality=lot_data.get("quality"),
        real_time_end_at=convert_game_date_to_real_date(lot_data["end_at"]),
    )


def _extract_lot_id(message) -> int:
    x = re.search("(?<=#)\d.*?(?=\D)", message)
    return int(x[0])  # type: ignore


def _extract_full_seller_name(message) -> str:
    x = re.search("(?<=Seller: ).*", message)
    return x[0]  # type: ignore


def _extract_current_price(message) -> int:
    x = re.search("(?<=price: ).*?(?= )", message)
    return int(x[0])  # type: ignore


def _extract_full_buyer_name(message) -> Optional[str]:
    x = re.search("(?<=Buyer: ).*", message)

    if x[0] != "None":  # type: ignore
        return x[0]  # type: ignore

    return None


def _extract_status(message) -> str:
    x = re.search("(?<=Status: ).*", message)
    return x[0]  # type: ignore


def _extract_end_at(message) -> str:
    x = re.search("(?<=End At: ).*", message)
    return x[0]  # type: ignore


def _extract_item(message) -> str:
    x = re.search("(?<=\d : ).*", message)
    return x[0]  # type: ignore


def _extract_quality(message) -> Optional[str]:
    x = re.search("(?<=Quality: ).*", message)

    if x:
        return x[0]  # type: ignore

    return None


def _split_name_and_castle(full_name: Optional[str]) -> Tuple:

    if not full_name:
        return None, None

    castle = full_name[0]
    name = full_name[1:].strip()

    return castle if castle else None, name if name else None


def _get_message_date(event):
    return event.message.date


def _get_status_int(status: str) -> int:

    dispatch = {"Finished": 2, "#active": 1, "Cancelled": 3, "Failed": 4, "#starting": 1}

    return dispatch[status]


def _get_quality_int(quality) -> int:

    dispatch = {"Fine": 1, "High": 2, "Great": 3, "Excellent": 4, "Masterpiece": 5, "Epic High": 6, "Epic Fine": 7}
    return dispatch[quality]


def _build_data(message) -> Dict:

    seller_castle, seller_name = _split_name_and_castle(_extract_full_seller_name(message))
    buyer_castle, buyer_name = _split_name_and_castle(_extract_full_buyer_name(message))

    auction_item = _extract_item(message)
    cleaned_item = cleaner_item_name(auction_item)

    data = {
        "lot_id": _extract_lot_id(message),
        "seller_name": seller_name,
        "seller_castle": seller_castle,
        "price": _extract_current_price(message),
        "buyer_name": buyer_name,
        "buyer_castle": buyer_castle,
        "status": _get_status_int(_extract_status(message)),
        "end_at": _extract_end_at(message),
        "item": cleaned_item,
        "auction_item": auction_item,
    }

    quality = _extract_quality(message)

    if quality:
        data["quality"] = _get_quality_int(quality)

    return data


def convert_game_date_to_real_date(game_date: str):
    GAME_TIME_OFFSET = 33281420544
    months = {
        "Wintar": 1,
        "Hornung": 2,
        "Lenzin": 3,
        "Ōstar": 4,
        "Winni": 5,
        "Brāh": 6,
        "Hewi": 7,
        "Aran": 8,
        "Witu": 9,
        "Wīndume": 10,
        "Herbist": 11,
        "Hailag": 12,
    }

    r = game_date.split(" ")
    t = r[3].split(":")
    d = f"{r[0]}-{months[r[1]]}-{r[2]} {t[0]}:{t[1]}"

    date_time_obj = datetime.datetime.strptime(d, "%d-%m-%Y %H:%M")

    x = (date_time_obj.timestamp() + GAME_TIME_OFFSET) / 3
    dt_object = datetime.datetime.fromtimestamp(x)

    return make_aware(dt_object)
