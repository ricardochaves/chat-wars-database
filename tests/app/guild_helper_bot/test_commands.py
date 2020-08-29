from django.test import TestCase

from chat_wars_database.app.guild_helper_bot.business.commands import command_alliance_info
from chat_wars_database.app.guild_helper_bot.models import Alliance
from chat_wars_database.app.guild_helper_bot.models import Guild
from chat_wars_database.app.guild_helper_bot.models import TelegramUser
from chat_wars_database.app.guild_helper_bot.models import UserGuild


class TestGuild(TestCase):
    def setUp(self) -> None:
        self.telegram_user_captain = TelegramUser.objects.create(name="Ricardo", user_name="ricardo", telegram_id=123)
        self.guild = Guild.objects.create(name="guild_name_test", captain=self.telegram_user_captain)
        self.alliance = Alliance.objects.create(name="alliance_name_test", owner=self.guild)
        self.guild.alliance = self.alliance
        self.guild.save()
        self.user_guild = UserGuild.objects.create(user=self.telegram_user_captain, guild=self.guild)

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
