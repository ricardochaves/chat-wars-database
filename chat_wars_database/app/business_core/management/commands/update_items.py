import datetime
import logging
from time import sleep
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

import requests
from django.core.management import BaseCommand
from django.utils.timezone import make_aware

from chat_wars_database.app.business_core.models import Category
from chat_wars_database.app.business_core.models import Item

logger = logging.getLogger(__name__)


def mount_item_name_for_querystring(item_name: str) -> str:
    n = item_name.title()

    if "📙" in n:
        n = n.replace("📙", "")
        n += " (Orange)"

    if "📕" in n:
        n = n.replace("📕", "")
        n += " (Red)"

    if "📗" in n:
        n = n.replace("📗", "")
        n += " (Green)"

    if "📘" in n:
        n = n.replace("📘", "")
        n += " (Blue)"

    n = n.replace(" ", "-20")
    n = n.replace("Of", "of")

    return n


def find_and_return_value(
    item_data: Dict, key: str, default: Optional[Union[str, int, bool, datetime.datetime]] = None
) -> Optional[Union[str, int, bool, datetime.datetime]]:

    for x in item_data["data"]:
        if x["property"] == key:
            if x["dataitem"][0]["type"] == 4:

                return x["dataitem"][0]["item"] == "t"
            if x["dataitem"][0]["type"] == 2:
                return x["dataitem"][0]["item"]

            if x["dataitem"][0]["type"] == 9:
                return x["dataitem"][0]["item"].split("#")[0]

            if x["dataitem"][0]["type"] == 1:
                return int(x["dataitem"][0]["item"])

            if x["dataitem"][0]["type"] == 6:
                d = x["dataitem"][0]["item"].split("/")
                return make_aware(datetime.datetime(int(d[1]), int(d[2]), int(d[3]), int(d[4]), int(d[5]), int(d[6])))

    return default


def find_and_return_list(item_data: Dict, key: str) -> List:
    for x in item_data["data"]:
        if x["property"] == key:

            if x["dataitem"][0]["type"] == 9:
                return x["dataitem"]

    return []


def update_categories(item: Item, data: Dict) -> None:

    cat_list = find_and_return_list(data, "_INST")

    item.categories.exclude()
    for c in cat_list:
        clean_name = c["item"].split("#")[0]
        defaults = {"name": clean_name}

        category, _ = Category.objects.get_or_create(name=clean_name, defaults=defaults)

        item.categories.add(category)


def get_item_data(item: Item) -> Dict:

    n = mount_item_name_for_querystring(item.name)
    url = f"https://chatwars-wiki.de/index.php?title=Special:Browse/:{n}&format=json"
    response = requests.get(url)
    assert response.status_code == 200
    return response.json()


def execute_item(item: Item) -> None:
    try:
        data = get_item_data(item)
    except BaseException as e:
        logger.warning("ERROR: %s", e)
        return

    if len(data["data"]) < 2:
        logger.warning("We dont have information about item: %s", item.name)
        return

    logger.info("Data: for item %s: %s", item.name, data)

    item.command = find_and_return_value(data, "ItemID")
    item.tradeable_exchange = find_and_return_value(data, "BoolExchange", False)
    item.tradeable_auction = find_and_return_value(data, "BoolAuction", False)
    item.craftable = find_and_return_value(data, "BoolCraft", False)
    item.depositable_in_guild = find_and_return_value(data, "BoolDepositGuild", False)
    item.event_item = find_and_return_value(data, "BoolEventItem", False)
    item.can_be_found_in_quests = find_and_return_value(data, "BoolQuest")
    item.craft_command = find_and_return_value(data, "CraftCommand")
    item.mana_crafting = find_and_return_value(data, "ManaCrafting")
    item.skill_craft_level = find_and_return_value(data, "SkillCraftLevel")
    item.weight = find_and_return_value(data, "Weight")
    item.modification_date = find_and_return_value(data, "_MDAT")
    item.base_duration = find_and_return_value(data, "BaseDuration")

    item.quest_forest_day = find_and_return_value(data, "QuestForestDay")
    item.quest_swamp_day = find_and_return_value(data, "QuestSwampDay")
    item.quest_valley_day = find_and_return_value(data, "QuestValleyDay")
    item.quest_foray_day = find_and_return_value(data, "QuestForayDay")
    item.quest_forest_morning = find_and_return_value(data, "QuestForestMorning")
    item.quest_swamp_morning = find_and_return_value(data, "QuestSwampMorning")
    item.quest_valley_morning = find_and_return_value(data, "QuestValleyMorning")
    item.quest_foray_morning = find_and_return_value(data, "QuestForayMorning")
    item.quest_forest_evening = find_and_return_value(data, "QuestForestEvening")
    item.quest_swamp_evening = find_and_return_value(data, "QuestSwampEvening")
    item.quest_valley_evening = find_and_return_value(data, "QuestValleyEvening")
    item.quest_foray_evening = find_and_return_value(data, "QuestForayEvening")
    item.quest_forest_night = find_and_return_value(data, "QuestForestNight")
    item.quest_swamp_night = find_and_return_value(data, "QuestSwampNight")
    item.quest_valley_night = find_and_return_value(data, "QuestValleyNight")
    item.quest_foray_night = find_and_return_value(data, "QuestForayNight")

    update_categories(item, data)

    item.save()


class Command(BaseCommand):
    def handle(self, *args, **options):

        items = Item.objects.all()

        for i in items:
            sleep(2)
            logger.info("Item name: %s", i.name)
            execute_item(i)
