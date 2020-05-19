from django.test import TestCase

from chat_wars_database.app.business_core.models import Item
from chat_wars_database.app.business_core.models import Recipe
from chat_wars_database.app.craft.business import create_message
from chat_wars_database.app.craft.business import update_all_crafted_items


class TestCraftBusiness(TestCase):
    def setUp(self) -> None:
        self.ITEM_COMMAND = "28"
        Item.objects.create(name="Silver mold", command=self.ITEM_COMMAND, craftable=True)
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

    def test_create_message(self):
        update_all_crafted_items()

        message = create_message(self.ITEM_COMMAND)
        self.assertIsNot(message, "")
