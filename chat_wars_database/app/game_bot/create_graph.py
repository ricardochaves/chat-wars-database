import logging
import uuid
from datetime import timedelta
from typing import Dict

import matplotlib.pyplot as plt
from django.db.models import Avg
from django.db.models.functions import TruncDate
from django.utils import timezone

from chat_wars_database.app.business_auction.models import AuctionLot
from chat_wars_database.app.business_core.models import Item
from chat_wars_database.app.game_bot.telegram_service import send_photo

logger = logging.getLogger(__name__)


def create_graph(message: Dict) -> None:
    """
    {"chat_id": 449256847, "item_command": "s07", "graph_time": 3}
    """
    photo_name = f"{uuid.uuid4().hex}.png"

    command = message["item_command"]
    total_days: int = message["graph_time"]

    limit_date = timezone.now() - timedelta(days=total_days)
    chat_id = message["chat_id"]

    item = Item.objects.filter(command=command).first()
    if not item:
        return

    items = (
        AuctionLot.objects.filter(item__command=command, message_date__gte=limit_date)
        .annotate(d=TruncDate("message_date"))
        .values("d")
        .annotate(Avg("price"))
    )

    if items:
        x = []
        y = []

        for i in items:
            x.append(i["price__avg"])
            y.append(i["d"])

        plt.ylabel("Value Prices")
        plt.xlabel("Date")
        plt.title(item.name)

        sub = plt.subplot(111)
        sub.bar(y, x, color=(0.2, 0.4, 0.6, 0.6))
        sub.xaxis_date()

        logger.info("Saving image...")
        plt.savefig(photo_name)

        graph_message: str = f"You are viewing a {total_days}-day chart. This is the average value of all actions with the status of finished per day."  # pylint: disable = line-too-long # noqa
        send_photo(graph_message, photo_name, chat_id)
