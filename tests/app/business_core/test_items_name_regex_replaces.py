from django.test import TestCase

from chat_wars_database.app.business_core.business import cleaner_item_name


class TestItemsCore(TestCase):
    def test_cleaner_item_name_should_replace_all_chars(self):
        self.assertEqual(cleaner_item_name("Clarity Robe +8⚔ +24🛡 +140💧"), "Clarity Robe")
        self.assertEqual(cleaner_item_name("Clarity Robe +8⚔ +24🛡"), "Clarity Robe")
        self.assertEqual(cleaner_item_name("Clarity Robe +8⚔ +140💧"), "Clarity Robe")
        self.assertEqual(cleaner_item_name("Clarity Robe +128⚔ +234🛡 +1400💧"), "Clarity Robe")
        self.assertEqual(cleaner_item_name("Clarity Robe +24🛡 +140💧"), "Clarity Robe")

        self.assertEqual(cleaner_item_name("Clarity Robe"), "Clarity Robe")
        self.assertEqual(cleaner_item_name("⚡+3 Clarity Robe"), "Clarity Robe")

        self.assertEqual(cleaner_item_name("⚡+3 Clarity Robe +24🛡 +140💧"), "Clarity Robe")
        self.assertEqual(cleaner_item_name("⚡+3 Clarity Robe +8⚔ +24🛡 +140💧"), "Clarity Robe")
        self.assertEqual(cleaner_item_name("⚡+3 Clarity Robe +8⚔ +24🛡"), "Clarity Robe")
        self.assertEqual(cleaner_item_name("⚡+3 Clarity Robe +8⚔ +140💧"), "Clarity Robe")
        self.assertEqual(cleaner_item_name("⚡+3 Clarity Robe +128⚔ +234🛡 +1400💧"), "Clarity Robe")

        self.assertEqual(cleaner_item_name("⚡+35 Clarity Robe +24🛡 +140💧"), "Clarity Robe")
        self.assertEqual(cleaner_item_name("⚡+35 Clarity Robe +8⚔ +24🛡 +140💧"), "Clarity Robe")
        self.assertEqual(cleaner_item_name("⚡+35 Clarity Robe +8⚔ +24🛡"), "Clarity Robe")
        self.assertEqual(cleaner_item_name("⚡+35 Clarity Robe +8⚔ +140💧"), "Clarity Robe")
        self.assertEqual(cleaner_item_name("⚡+35 Clarity Robe +128⚔ +234🛡 +1400💧"), "Clarity Robe")
        self.assertEqual(cleaner_item_name("⚡+35 Clarity Robe +128⚔ +234🛡 +1400💧"), "Clarity Robe")

        self.assertEqual(cleaner_item_name("📕Scroll of Peace"), "📕Scroll of Peace")
        self.assertEqual(cleaner_item_name("📗Scroll of Peace"), "📗Scroll of Peace")
