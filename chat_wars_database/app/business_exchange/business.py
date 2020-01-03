import datetime
from datetime import timedelta
from statistics import mean
from typing import Dict
from typing import Optional
from typing import Tuple

from django.utils import timezone

from chat_wars_database.app.business_core.models import Item
from chat_wars_database.app.business_exchange.models import StatsByDay


def _check_min_data(min_value, dt_value, s: StatsByDay) -> Tuple[int, datetime.date]:
    if min_value == 1:
        return 1, dt_value

    if min_value == 0:
        return s.min_value, s.date

    if min_value > s.min_value:
        return s.min_value, s.date

    return min_value, dt_value


def _check_max_data(max_value, dt_value, s: StatsByDay) -> Tuple[int, datetime.date]:

    if max_value == 0:
        return s.max_value, s.date

    if max_value < s.max_value:
        return s.max_value, s.date

    return max_value, dt_value


def get_exchange_data(item: Item) -> Optional[Dict]:

    dt = timezone.now() - timedelta(days=30)

    stats = StatsByDay.objects.filter(item=item, date__gte=dt).all()
    if not stats:
        return None

    data: Dict = {
        "avg_price_30_days": 0,
        "total_sold": 0,
        "min_value": 0,
        "min_value_date": None,
        "max_value": 0,
        "max_value_date": None,
        "deerhorn_castle_seller": 0,
        "dragonscale_castle_seller": 0,
        "highnest_castle_seller": 0,
        "moonlight_castle_seller": 0,
        "potato_castle_seller": 0,
        "sharkteeth_castle_seller": 0,
        "wolfpack_castle_seller": 0,
        "deerhorn_castle_buyer": 0,
        "dragonscale_castle_buyer": 0,
        "highnest_castle_buyer": 0,
        "moonlight_castle_buyer": 0,
        "potato_castle_buyer": 0,
        "sharkteeth_castle_buyer": 0,
        "wolfpack_castle_buyer": 0,
    }
    values = []
    for s in stats:

        min_value, min_value_data = _check_min_data(data["min_value"], data["min_value_date"], s)
        max_value, max_value_data = _check_max_data(data["max_value"], data["max_value_date"], s)

        data["total_sold"] += s.units
        data["min_value"] = min_value
        data["min_value_date"] = min_value_data
        data["max_value"] = max_value
        data["max_value_date"] = max_value_data

        data["deerhorn_castle_seller"] += s.deerhorn_castle_seller
        data["dragonscale_castle_seller"] += s.dragonscale_castle_seller
        data["highnest_castle_seller"] += s.highnest_castle_seller
        data["moonlight_castle_seller"] += s.moonlight_castle_seller
        data["potato_castle_seller"] += s.potato_castle_seller
        data["sharkteeth_castle_seller"] += s.sharkteeth_castle_seller
        data["wolfpack_castle_seller"] += s.wolfpack_castle_seller
        data["deerhorn_castle_buyer"] += s.deerhorn_castle_buyer
        data["dragonscale_castle_buyer"] += s.dragonscale_castle_buyer
        data["highnest_castle_buyer"] += s.highnest_castle_buyer
        data["moonlight_castle_buyer"] += s.moonlight_castle_buyer
        data["potato_castle_buyer"] += s.potato_castle_buyer
        data["sharkteeth_castle_buyer"] += s.sharkteeth_castle_buyer
        data["wolfpack_castle_buyer"] += s.wolfpack_castle_buyer

        values.append(s.average_value)

    data["avg_price_30_days"] = round(mean(values), 2)

    return data
