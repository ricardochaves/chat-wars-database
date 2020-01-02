import datetime
import logging
import uuid
from datetime import timedelta
from typing import Dict
from typing import List

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from django.db.models import Avg
from django.db.models.functions import TruncDate
from django.utils import timezone

from chat_wars_database.app.business_auction.models import AuctionLot
from chat_wars_database.app.business_core.models import Item
from chat_wars_database.app.business_exchange.models import StatsByDay
from chat_wars_database.app.game_bot.pubsub_service import sent_message
from chat_wars_database.app.game_bot.telegram_service import send_photo

logger = logging.getLogger(__name__)


def send_graph_message(chat_id: str, text: str) -> None:
    item_command = text.split("_")[1]
    graph_time = 700
    try:
        graph_time = int(text.split("_")[2])
    except BaseException:
        pass

    data = {"chat_id": chat_id, "item_command": item_command, "graph_time": graph_time}

    sent_message(data)


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

    if item.tradeable_auction:
        create_graph_for_auction(item, limit_date, photo_name)
    elif item.tradeable_exchange:
        create_graph_for_exchange(item, limit_date, photo_name)

    graph_message: str = f"You are viewing a {total_days}-day chart. This is the average value of all actions with the status of finished per day."  # pylint: disable = line-too-long # noqa
    send_photo(graph_message, photo_name, chat_id)


def create_graph_for_auction(item: Item, limit_date: datetime.datetime, photo_name: str) -> None:

    items = (
        AuctionLot.objects.filter(item=item, message_date__gte=limit_date)
        .annotate(d=TruncDate("message_date"))
        .values("d")
        .annotate(Avg("price"))
    )

    if items:
        x = []
        y = []

        for i in items:
            y.append(i["price__avg"])
            x.append(i["d"])

        plot_graph(x, y, "Date", "Average Price", item.name, photo_name)


def create_graph_for_exchange(item: Item, limit_date: datetime.datetime, photo_name: str) -> None:

    items = StatsByDay.objects.filter(item=item, date__gte=limit_date).all()

    if items:
        x = []
        y = []

        for i in items:
            y.append(i.average_value)
            x.append(i.date)

        plot_graph(x, y, "Date", "Average Price", item.name, photo_name)


def plot_graph(  # pylint: disable = too-many-arguments
    x: List, y: List, xlabel: str, ylabel: str, title: str, file_name: str
) -> None:

    _, ax = plt.subplots(figsize=(12, 8))
    # _.autofmt_xdate(rotation=45)

    ax.bar(x, y, color="blue")

    ax.set(xlabel=xlabel, ylabel=ylabel, title=title)

    locator = mdates.AutoDateLocator(minticks=3, maxticks=7)
    formatter = mdates.ConciseDateFormatter(locator)

    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)

    logger.info("Saving image...")
    plt.savefig(file_name)

    plt.clf()
    plt.cla()
    plt.close()
