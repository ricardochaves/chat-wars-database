import datetime
import logging
import re
from statistics import mean
from statistics import median
from typing import Dict
from typing import List
from typing import Tuple

from django.core.management import BaseCommand
from django.utils import timezone

from chat_wars_database.app.business_core.business import get_or_create_item
from chat_wars_database.app.business_exchange.models import ExchangeMessages
from chat_wars_database.app.business_exchange.models import StatsByDay

logger = logging.getLogger(__name__)


def get_max_value_date(values_by_list: List[Dict]) -> Tuple[int, int]:
    """
    {"value": 100, "message_id": 1234]}
    """

    v = 0
    m = 0

    for x in values_by_list:
        check = v < x["value"]

        v = x["value"] if check else v
        m = x["message_id"] if check else m

    return v, m


def get_min_value_date(values_by_list: List[Dict]) -> Tuple[int, int]:
    """
    {"value": 100, "message_id": 1234]}
    """

    v = values_by_list[0]["value"]
    m = values_by_list[0]["message_id"]

    for x in values_by_list:
        check = v > x["value"]
        v = x["value"] if check else v
        m = x["message_id"] if check else m

    return v, m


def apply_regex_for_each_line(line: str):

    m = re.search(r"=> .*, (?P<quantity>\d*) ?(?=x)x (?P<value>\d*)?(?=💰)", line)

    return m


def calculate(dt: datetime.date) -> None:
    exchanges = ExchangeMessages.objects.filter(message_date__date=dt).all()
    data: Dict = {}
    item_name = ""

    for e in exchanges:

        lines = e.message_text.split("\n")

        for line in lines:
            match = re.match(r"(.*):", line)

            if match:
                item_name = match[1]
                if not data.get(item_name):
                    data[item_name] = []

            else:
                data[item_name].append({"line": line, "message_id": e.message_id})

    for k in data:

        item = get_or_create_item(k)

        stats_by_item: Dict = {
            "date": dt,
            "item": item,
            "units": 0,
            "average_value": 0,
            "mean_value": 0,
            "min_value": 0,
            "max_value": 0,
            "min_value_message_id": 0,
            "max_value_message_id": 0,
            "deerhorn_castle_seller": 0,
            "deerhorn_castle_buyer": 0,
            "dragonscale_castle_seller": 0,
            "dragonscale_castle_buyer": 0,
            "highnest_castle_seller": 0,
            "highnest_castle_buyer": 0,
            "moonlight_castle_seller": 0,
            "moonlight_castle_buyer": 0,
            "potato_castle_seller": 0,
            "potato_castle_buyer": 0,
            "sharkteeth_castle_seller": 0,
            "sharkteeth_castle_buyer": 0,
            "wolfpack_castle_seller": 0,
            "wolfpack_castle_buyer": 0,
        }

        values_by_list: List[Dict] = []
        for line_dict in data[k]:
            line = line_dict["line"]
            m = apply_regex_for_each_line(line)

            qtd = int(m.group("quantity"))

            for v in range(qtd):
                values_by_list.append({"value": int(m.group("value")), "message_id": line_dict["message_id"]})

            stats_by_item["units"] += qtd
            stats_by_item["deerhorn_castle_seller"] += qtd if line[0] == "🦌" else 0
            stats_by_item["deerhorn_castle_buyer"] += qtd if m.group()[3] == "🦌" else 0
            stats_by_item["dragonscale_castle_seller"] += qtd if line[0] == "🐉" else 0
            stats_by_item["dragonscale_castle_buyer"] += qtd if m.group()[3] == "🐉" else 0
            stats_by_item["highnest_castle_seller"] += qtd if line[0] == "🦅" else 0
            stats_by_item["highnest_castle_buyer"] += qtd if m.group()[3] == "🦅" else 0
            stats_by_item["moonlight_castle_seller"] += qtd if line[0] == "🌑" else 0
            stats_by_item["moonlight_castle_buyer"] += qtd if m.group()[3] == "🌑" else 0
            stats_by_item["potato_castle_seller"] += qtd if line[0] == "🥔" else 0
            stats_by_item["potato_castle_buyer"] += qtd if m.group()[3] == "🥔" else 0
            stats_by_item["sharkteeth_castle_seller"] += qtd if line[0] == "🦈" else 0
            stats_by_item["sharkteeth_castle_buyer"] += qtd if m.group()[3] == "🦈" else 0
            stats_by_item["wolfpack_castle_seller"] += qtd if line[0] == "🐺" else 0
            stats_by_item["wolfpack_castle_buyer"] += qtd if m.group()[3] == "🐺" else 0

        v, m = get_max_value_date(values_by_list)
        stats_by_item["max_value"] = v
        stats_by_item["max_value_message_id"] = m

        v, m = get_min_value_date(values_by_list)
        stats_by_item["min_value"] = v
        stats_by_item["min_value_message_id"] = m

        ns = [v["value"] for v in values_by_list]  # type: ignore
        stats_by_item["average_value"] = round(mean(ns), 2)
        stats_by_item["mean_value"] = median(ns)

        StatsByDay.objects.update_or_create(item=item, date=dt, defaults=stats_by_item)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("total_days", type=int)  # 465 days to process all database

    def handle(self, *args, **options):
        stop_at = (datetime.datetime.now() + datetime.timedelta(days=-options["total_days"])).date()
        start_at = datetime.datetime.now().date() + datetime.timedelta(days=-1)
        logger.info("stop_at %s and start_at %s", stop_at, start_at)

        if start_at <= stop_at:
            logger.info("Start_at <= stop_at... Done...")
            return

        logger.info("Start loop now with dt: %s and %s", stop_at, timezone.now().date())
        while start_at > stop_at:
            logger.info("Calculate now: %s", start_at)
            calculate(start_at)
            start_at = start_at + datetime.timedelta(days=-1)

        logger.info("Done ")
