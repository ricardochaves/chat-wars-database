from datetime import datetime

from django.test import TestCase

from chat_wars_database.app.guild_helper_bot.business.commands import command_alliance_info
from chat_wars_database.app.guild_helper_bot.commands import _execute_found_hidden_location_or_headquarter
from chat_wars_database.app.guild_helper_bot.commands import _get_headquarter_and_build_message
from chat_wars_database.app.guild_helper_bot.commands import _get_locations_and_build_message
from chat_wars_database.app.guild_helper_bot.models import Alliance
from chat_wars_database.app.guild_helper_bot.models import Guild
from chat_wars_database.app.guild_helper_bot.models import HiddenHeadquarter
from chat_wars_database.app.guild_helper_bot.models import HiddenLocation
from chat_wars_database.app.guild_helper_bot.models import HiddenMessage
from chat_wars_database.app.guild_helper_bot.models import TelegramUser
from chat_wars_database.app.guild_helper_bot.models import UserDeposits
from chat_wars_database.app.guild_helper_bot.models import UserGuild


class TestGuild(TestCase):
    def setUp(self) -> None:
        self.telegram_user_captain = TelegramUser.objects.create(name="Ricardo", user_name="ricardo", telegram_id=123)
        self.guild = Guild.objects.create(name="guild_name_test", captain=self.telegram_user_captain)
        self.alliance = Alliance.objects.create(name="alliance_name_test", owner=self.guild)
        self.guild.alliance = self.alliance
        self.guild.save()
        self.user_guild = UserGuild.objects.create(user=self.telegram_user_captain, guild=self.guild)

        self.hidden_message = HiddenMessage.objects.create(
            chat_id=123,
            forward_date=datetime.now(),
            telegram_user=self.telegram_user_captain,
            message_text="234",
            message_id=234,
        )

    def test_should_return_alliance_info(self):
        expected_message = f"""alliance_name_test
Guilds: 1 👥 1
Owner: guild_name_test"""

        message = command_alliance_info(self.telegram_user_captain)

        self.assertEqual(message, expected_message)

    def test_should_return_user_dont_have_guild(self):
        fake_user = TelegramUser.objects.create(name="ZPT_XPTO", user_name="asd", telegram_id=456)
        expected_message = f"You don't have any guild. Use /create_guild <name>"

        message = command_alliance_info(fake_user)

        self.assertEqual(message, expected_message)

    def test_should_return_guild_dont_have_alliance(self):

        expected_message = "Your guild does not have an alliance"

        self.guild.alliance = None
        self.guild.save()

        message = command_alliance_info(self.telegram_user_captain)

        self.assertEqual(message, expected_message)

    def test_execute_found_hidden_location_or_headquarter_should_add_new_location(self):
        message_text = """You found hidden location Ancient Ruins lvl.60
You noticed that objective is captured by alliance.
То remember the route you associated it with simple combination: DmVnRJ"""
        telegram_user_data = {
            "user_name": "@ricardo",
            "name": "ricardo",
            "telegram_id": 123,
        }

        message_data = {
            "chat_id": 456,
            "forward_date": datetime.now(),
            "message_text": message_text,
            "message_id": 987,
        }
        HiddenMessage.objects.all().delete()

        _execute_found_hidden_location_or_headquarter(telegram_user_data, message_data)

        self.assertEqual(HiddenMessage.objects.count(), 1)
        self.assertEqual(HiddenLocation.objects.count(), 1)
        self.assertEqual(UserDeposits.objects.count(), 0)

        hidden_location = HiddenLocation.objects.first()
        self.assertEqual(hidden_location.combination, "DmVnRJ")
        self.assertEqual(hidden_location.lvl, 60)

    def test_execute_found_hidden_location_or_headquarter_should_add_new_headquarter(self):
        message_text = """You found hidden headquarter Heavy Star
То remember the route you associated it with simple combination: d5shvW"""

        telegram_user_data = {
            "user_name": "@ricardo",
            "name": "ricardo",
            "telegram_id": 123,
        }

        message_data = {
            "chat_id": 456,
            "forward_date": datetime.now(),
            "message_text": message_text,
            "message_id": 987,
        }
        HiddenMessage.objects.all().delete()

        _execute_found_hidden_location_or_headquarter(telegram_user_data, message_data)

        self.assertEqual(HiddenMessage.objects.count(), 1)
        self.assertEqual(HiddenHeadquarter.objects.count(), 1)
        self.assertEqual(UserDeposits.objects.count(), 0)

        hidden_headquarter = HiddenHeadquarter.objects.first()
        self.assertEqual(hidden_headquarter.combination, "d5shvW")

    def test_should_return_locations_message(self):
        fake_user = TelegramUser.objects.create(name="ZPT_XPTO", user_name="asd", telegram_id=456)
        HiddenLocation.objects.create(
            telegram_user=self.telegram_user_captain,
            message=self.hidden_message,
            name="location_1",
            lvl=50,
            combination="Xk3jr",
        )
        HiddenLocation.objects.create(
            telegram_user=self.telegram_user_captain,
            message=self.hidden_message,
            name="location_2",
            lvl=55,
            combination="K3kDr",
        )
        HiddenLocation.objects.create(
            telegram_user=fake_user, message=self.hidden_message, name="location_2", lvl=10, combination="KRU8OL"
        )

        expected_message = """Locations:
location_2 lvl 55 - K3kDr
location_1 lvl 50 - Xk3jr
"""

        message = _get_locations_and_build_message(self.telegram_user_captain)

        self.assertEqual(message, expected_message)

    def test_should_return_headquarter_message(self):
        fake_user = TelegramUser.objects.create(name="ZPT_XPTO", user_name="asd", telegram_id=456)
        HiddenHeadquarter.objects.create(
            telegram_user=self.telegram_user_captain,
            message=self.hidden_message,
            name="headquarter_1",
            combination="Xk3jr",
        )
        HiddenHeadquarter.objects.create(
            telegram_user=self.telegram_user_captain,
            message=self.hidden_message,
            name="headquarter_2",
            combination="K3kDr",
        )
        HiddenHeadquarter.objects.create(
            telegram_user=fake_user, message=self.hidden_message, name="headquarter_3", combination="KRU8OL"
        )

        expected_message = """Headquarters:
headquarter_2 - K3kDr
headquarter_1 - Xk3jr
"""

        message = _get_headquarter_and_build_message(self.telegram_user_captain)

        self.assertEqual(message, expected_message)
