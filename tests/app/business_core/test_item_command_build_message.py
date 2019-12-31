from django.test import TestCase

from chat_wars_database.app.business_core.business import build_message
from chat_wars_database.app.business_core.models import Category
from chat_wars_database.app.business_core.models import Item


class TestItemsCore(TestCase):
    def test_execute_build_message_without_error_i1(self):

        item = Item.objects.create(name="Potion of Rage")
        build_message(item)

    def test_execute_build_message_without_error_i2(self):

        item = Item.objects.create(
            name="Potion of Rage",
            command="r12",
            tradeable_exchange=True,
            tradeable_auction=False,
            craftable=True,
            depositable_in_guild=False,
            event_item=True,
            can_be_found_in_quests=False,
            craft_command="/craft_r12",
            mana_crafting=12,
            skill_craft_level=1,
            weight=2,
            base_duration=20,
        )
        build_message(item)

    def test_execute_build_message_without_error_i3(self):
        cat = Category.objects.create(name="c1")
        item = Item.objects.create(
            name="Potion of Rage",
            command="r12",
            tradeable_exchange=True,
            tradeable_auction=False,
            craftable=True,
            depositable_in_guild=False,
            event_item=True,
            can_be_found_in_quests=False,
            craft_command="/craft_r12",
            mana_crafting=12,
            skill_craft_level=1,
            weight=2,
            base_duration=20,
        )
        item.categories.add(cat)
        item.save()
        build_message(item)

    def test_execute_build_message_without_error_i4(self):
        cat1 = Category.objects.create(name="c1")
        cat2 = Category.objects.create(name="c2")

        item = Item.objects.create(
            name="Potion of Rage",
            command="r12",
            tradeable_exchange=True,
            tradeable_auction=False,
            craftable=True,
            depositable_in_guild=False,
            event_item=True,
            can_be_found_in_quests=False,
            craft_command="/craft_r12",
            mana_crafting=12,
            skill_craft_level=1,
            weight=2,
            base_duration=20,
        )
        item.categories.add(cat1)
        item.categories.add(cat2)

        item.save()
        build_message(item)

    def test_execute_build_message_without_error_i5(self):
        cat1 = Category.objects.create(name="c1")
        cat2 = Category.objects.create(name="c2")

        item = Item.objects.create(
            name="Potion of Rage",
            command="r12",
            tradeable_exchange=True,
            tradeable_auction=False,
            craftable=True,
            depositable_in_guild=False,
            event_item=True,
            can_be_found_in_quests=False,
            craft_command="/craft_r12",
            mana_crafting=12,
            skill_craft_level=1,
            weight=2,
            base_duration=20,
            quest_forest_day=False,
            quest_swamp_day=False,
            quest_valley_day=False,
            quest_foray_day=False,
            quest_forest_morning=False,
            quest_swamp_morning=True,
            quest_valley_morning=False,
            quest_foray_morning=False,
            quest_forest_evening=False,
            quest_swamp_evening=False,
            quest_valley_evening=False,
            quest_foray_evening=False,
            quest_forest_night=False,
            quest_swamp_night=False,
            quest_valley_night=False,
            quest_foray_night=False,
        )
        item.categories.add(cat1)
        item.categories.add(cat2)

        item.save()
        build_message(item)
