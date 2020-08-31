import uuid

from django.db import IntegrityError
from django.test import TestCase

from chat_wars_database.app.guild_helper_bot.business.alliance import get_all_chats_for_alliance_atack_orders
from chat_wars_database.app.guild_helper_bot.business.guild import create_guild
from chat_wars_database.app.guild_helper_bot.business.guild import create_invite_member_link
from chat_wars_database.app.guild_helper_bot.business.guild import delete_guild
from chat_wars_database.app.guild_helper_bot.business.guild import update_guild_name
from chat_wars_database.app.guild_helper_bot.business.guild import use_invited_id_link
from chat_wars_database.app.guild_helper_bot.business.telegram_user import create_telegram_user_if_need
from chat_wars_database.app.guild_helper_bot.models import Guild
from chat_wars_database.app.guild_helper_bot.models import InvitationLink
from chat_wars_database.app.guild_helper_bot.models import UserGuild
from tests.app.helper import add_guild_to_alliance
from tests.app.helper import create_alliance
from tests.app.helper import create_guild_channel
from tests.app.helper import create_telegram_user
from tests.app.helper import create_user_guild


class TestGuild(TestCase):
    def setUp(self) -> None:
        self.guild_name = "test_name"
        self.telegram_user_1 = create_telegram_user("user_1", "@user_1", 12)
        self.telegram_user_2 = create_telegram_user("user_2", "@user_2", 13)
        self.telegram_user_3 = create_telegram_user("user_3", "@user_3", 14)

        self.guild_1 = create_guild("guild_1", self.telegram_user_1)
        self.guild_2 = create_guild("guild_2", self.telegram_user_2)
        self.guild_3 = create_guild("guild_3", self.telegram_user_3)

        self.alliance_1 = create_alliance("alliance_1", self.guild_1)
        add_guild_to_alliance(self.guild_1, self.alliance_1)
        add_guild_to_alliance(self.guild_2, self.alliance_1)

    def test_should_return_a_chat_list_with_ids(self):
        create_guild_channel(1, "c_1", True, self.guild_1)
        create_guild_channel(2, "c_2", False, self.guild_1)
        create_guild_channel(3, "c_3", True, self.guild_2)
        create_guild_channel(4, "c_4", True, self.guild_3)

        ids = get_all_chats_for_alliance_atack_orders(self.telegram_user_1)

        self.assertIn(1, ids)
        self.assertIn(3, ids)
        self.assertNotIn(2, ids)
        self.assertNotIn(4, ids)

    def test_should_return_a_empty_chat_list_when_guild_dont_have_alliance(self):
        ids = get_all_chats_for_alliance_atack_orders(self.telegram_user_3)
        self.assertEqual(ids, [])
