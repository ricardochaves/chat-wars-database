from django.test import TestCase

from chat_wars_database.app.business_core.models import Item
from chat_wars_database.app.business_core.models import Recipe
from chat_wars_database.app.craft.business import create_message
from chat_wars_database.app.craft.business import update_all_crafted_items


class TestCraftBusiness(TestCase):
    def setUp(self) -> None:
        self.ITEM_COMMAND = "29"
        Item.objects.create(name="Blacksmith frame", command=self.ITEM_COMMAND, craftable=True)
        Item.objects.create(name="Bauxite", craftable=False)
        Item.objects.create(name="Purified Powder", craftable=False)

        Item.objects.create(name="Silver mold", command="28", craftable=True)
        Item.objects.create(name="Silver Ore", craftable=False)
        Item.objects.create(name="Coke", craftable=False)
        Item.objects.create(name="String", craftable=False)

    def test_update_recipe_item(self):

        update_all_crafted_items()
        update_all_crafted_items()

        self.assertEqual(Recipe.objects.filter(item__command=self.ITEM_COMMAND).count(), 3)

        r_1 = Recipe.objects.filter(ingredient__name="Silver Ore").first()
        self.assertIsNotNone(r_1)
        self.assertEqual(r_1.amount, 2)

        r_2 = Recipe.objects.filter(ingredient__name="Coke").first()
        self.assertIsNotNone(r_2)
        self.assertEqual(r_2.amount, 2)

        r_3 = Recipe.objects.filter(ingredient__name="String").first()
        self.assertIsNotNone(r_3)
        self.assertEqual(r_3.amount, 2)

        r_4 = Recipe.objects.filter(ingredient__name="Silver mold").first()
        self.assertIsNotNone(r_4)
        self.assertEqual(r_4.amount, 1)

    def test_create_message(self):
        update_all_crafted_items()
        expected_message = """Recipe for Blacksmith frame updated at May 19 2020

`1 x Blacksmith frame
  5 x Bauxite
  3 x Purified Powder
  1 x Silver mold
    2 x Silver Ore
    2 x Coke
    2 x String
`"""

        message = create_message(self.ITEM_COMMAND)
        self.assertEqual(message, expected_message)
