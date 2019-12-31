from time import sleep

from django.test import TestCase

from chat_wars_database.app.business_core.management.commands.update_items import execute_item
from chat_wars_database.app.business_core.models import Category
from chat_wars_database.app.business_core.models import Item


class TestUpdateItems(TestCase):
    def test_execute_item_should_update_all_fields_when_find_data_i1(self):
        item = Item.objects.create(name="Wrapping")

        execute_item(item)

        item.refresh_from_db()

        self.assertTrue(item.craftable)

        self.assertFalse(item.tradeable_auction)
        self.assertFalse(item.depositable_in_guild)
        self.assertFalse(item.event_item)
        self.assertFalse(item.tradeable_exchange)
        self.assertFalse(item.can_be_found_in_quests)

        self.assertEqual(item.craft_command, "/craft_501")

        self.assertEqual(item.command, "501")
        self.assertEqual(item.mana_crafting, 10)
        self.assertEqual(item.weight, 2)
        self.assertEqual(item.categories.count(), 1)

        self.assertEqual(item.categories.first().name, "Resource")

    def test_execute_item_should_update_all_fields_when_find_data_i2(self):
        item = Item.objects.create(name="Potion of Rage")

        execute_item(item)
        sleep(1)
        execute_item(item)

        item.refresh_from_db()

        self.assertTrue(item.craftable)
        self.assertTrue(item.depositable_in_guild)
        self.assertTrue(item.tradeable_exchange)

        self.assertFalse(item.tradeable_auction)
        self.assertFalse(item.event_item)
        self.assertFalse(item.can_be_found_in_quests)

        self.assertEqual(item.base_duration, 30)
        self.assertEqual(item.mana_crafting, 15)
        self.assertEqual(item.skill_craft_level, 2)
        self.assertEqual(item.craft_command, "/brew_p02")
        self.assertEqual(item.command, "p02")

        self.assertEqual(item.categories.count(), 2)

        self.assertEqual(Category.objects.count(), 2)

    def test_execute_item_should_update_all_fields_when_find_data_i3(self):
        item = Item.objects.create(name="📙Scroll of Rage")

        execute_item(item)
