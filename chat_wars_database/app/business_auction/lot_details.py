import logging
from datetime import timedelta
from statistics import mean
from statistics import median
from typing import Dict

from django.utils import timezone

from chat_wars_database.app.business_auction.models import AuctionLot
from chat_wars_database.app.business_core.models import Item
from chat_wars_database.app.web.db_results import get_cheaper_lot
from chat_wars_database.app.web.db_results import get_first_lot
from chat_wars_database.app.web.db_results import get_last_lot
from chat_wars_database.app.web.db_results import get_more_expensive

logger = logging.getLogger(__name__)


def get_item_lot_details(item: Item) -> Dict:

    lots = AuctionLot.objects.filter(item=item).order_by("real_time_end_at").all()
    logger.info("Ok, I have the lots")

    total_life = 0
    total_life_sold = 0
    total_life_unsold = 0
    values_life = []

    total_week = 0
    total_week_sold = 0
    total_week_unsold = 0
    values_week = []

    last_sold = lots.last()

    for l in lots:

        total_life += 1

        if l.buyer_castle:
            total_life_sold += 1
            values_life.append(l.price)
        else:
            total_life_unsold += 1

        if l.message_date > (timezone.now() - timedelta(days=7)):

            total_week += 1

            if l.buyer_castle:
                total_week_sold += 1
                values_week.append(l.price)
            else:
                total_week_unsold += 1

    return {
        "total_life": total_life,
        "total_life_sold": total_life_sold,
        "total_life_unsold": total_life_unsold,
        "total_life_median": median(values_life) if values_life else 0,
        "total_life_average": round(mean(values_life), 2) if values_life else 0,
        "total_life_min": min(values_life) if values_life else 0,
        "total_life_max": max(values_life) if values_life else 0,
        "total_week": total_week,
        "total_week_sold": total_week_sold,
        "total_week_unsold": total_week_unsold,
        "total_week_median": median(values_week) if values_week else 0,
        "total_week_average": round(mean(values_week), 2) if values_week else 0,
        "total_week_min": min(values_week) if values_week else 0,
        "total_week_max": max(values_week) if values_week else 0,
        "last_sold": last_sold.price if last_sold else 0,
        "first_lot": get_first_lot(item.command),
        "last_lot": get_last_lot(item.command),
        "cheaper_lot": get_cheaper_lot(item.command),
        "more_expensive": get_more_expensive(item.command),
    }
