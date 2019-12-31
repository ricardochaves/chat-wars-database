import datetime
import logging
from time import sleep
from typing import Dict
from typing import Optional
from typing import Union

import requests
from django.core.management import BaseCommand
from django.utils.timezone import make_aware

from chat_wars_database.app.business_core.models import Item

logger = logging.getLogger(__name__)


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


def get_item_data(item: Item) -> Dict:

    n = item.name.title().replace(" ", "-20")
    url = f"https://chatwars-wiki.de/index.php?title=Special:Browse/:{n}&format=json"
    response = requests.get(url)
    assert response.status_code == 200
    return response.json()


class Command(BaseCommand):
    def handle(self, *args, **options):

        items = Item.objects.all()

        for i in items:
            sleep(2)
            logger.info("Item name: %s", i.name)
            try:
                data = get_item_data(i)
            except BaseException as e:
                logger.warning("ERROR: %s", e)
                continue

            logger.info("Data: for item %s: %s", i.name, data)

            i.command = find_and_return_value(data, "ItemID")
            i.tradeable_exchange = find_and_return_value(data, "BoolExchange", False)
            i.tradeable_auction = find_and_return_value(data, "BoolAuction", False)
            i.craftable = find_and_return_value(data, "BoolCraft", False)
            i.depositable_in_guild = find_and_return_value(data, "BoolDepositGuild", False)
            i.event_item = find_and_return_value(data, "BoolEventItem", False)
            i.can_be_found_in_quests = find_and_return_value(data, "BoolQuest")
            i.craft_command = find_and_return_value(data, "CraftCommand")
            i.item_type = find_and_return_value(data, "ItemType")
            i.mana_crafting = find_and_return_value(data, "ManaCrafting")
            i.skill_craft_level = find_and_return_value(data, "SkillCraftLevel")
            i.weight = find_and_return_value(data, "Weight")
            i.modification_date = find_and_return_value(data, "_MDAT")

            i.quest_forest_day = find_and_return_value(data, "QuestForestDay")
            i.quest_swamp_day = find_and_return_value(data, "QuestSwampDay")
            i.quest_valley_day = find_and_return_value(data, "QuestValleyDay")
            i.quest_foray_day = find_and_return_value(data, "QuestForayDay")
            i.quest_forest_morning = find_and_return_value(data, "QuestForestMorning")
            i.quest_swamp_morning = find_and_return_value(data, "QuestSwampMorning")
            i.quest_valley_morning = find_and_return_value(data, "QuestValleyMorning")
            i.quest_foray_morning = find_and_return_value(data, "QuestForayMorning")
            i.quest_forest_evening = find_and_return_value(data, "QuestForestEvening")
            i.quest_swamp_evening = find_and_return_value(data, "QuestSwampEvening")
            i.quest_valley_evening = find_and_return_value(data, "QuestValleyEvening")
            i.quest_foray_evening = find_and_return_value(data, "QuestForayEvening")
            i.quest_forest_night = find_and_return_value(data, "QuestForestNight")
            i.quest_swamp_night = find_and_return_value(data, "QuestSwampNight")
            i.quest_valley_night = find_and_return_value(data, "QuestValleyNight")
            i.quest_foray_night = find_and_return_value(data, "QuestForayNight")

            i.save()
