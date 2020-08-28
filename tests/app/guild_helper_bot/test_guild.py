import uuid

from django.db import IntegrityError
from django.test import TestCase

from chat_wars_database.app.guild_helper_bot.business.guild import create_guild
from chat_wars_database.app.guild_helper_bot.business.guild import create_invite_member_link
from chat_wars_database.app.guild_helper_bot.business.guild import delete_guild
from chat_wars_database.app.guild_helper_bot.business.guild import update_guild_name
from chat_wars_database.app.guild_helper_bot.business.guild import use_invited_id_link
from chat_wars_database.app.guild_helper_bot.business.telegram_user import create_telegram_user_if_need
from chat_wars_database.app.guild_helper_bot.models import Guild
from chat_wars_database.app.guild_helper_bot.models import InvitationLink
from chat_wars_database.app.guild_helper_bot.models import UserGuild


class TestGuild(TestCase):
    def setUp(self) -> None:
        self.guild_name = "test_name"
        self.telegram_user = create_telegram_user_if_need(1234, "test_name", "test_user_name")
        self.telegram_user_2 = create_telegram_user_if_need(567, "test_name", "test_user_name")

    def test_should_create_new_guild(self):

        guild = create_guild(self.guild_name, self.telegram_user)

        self.assertEqual(Guild.objects.count(), 1)
        self.assertEqual(guild.name, self.guild_name)
        self.assertEqual(guild.captain.telegram_id, self.telegram_user.telegram_id)
        self.assertEqual(UserGuild.objects.filter(guild=guild).count(), 1)

    def test_should_create_guild_raise_integrity_error_exists(self):
        create_guild(self.guild_name, self.telegram_user)
        with self.assertRaises(IntegrityError):
            create_guild(self.guild_name, self.telegram_user)

    def test_should_delete_guild(self):

        create_guild(self.guild_name, self.telegram_user)
        self.assertEqual(Guild.objects.filter(name__exact=self.guild_name).count(), 1)

        delete_guild(self.telegram_user)
        self.assertEqual(Guild.objects.filter(name__exact=self.guild_name).count(), 0)

    def test_should_update_guild_name(self):
        create_guild(self.guild_name, self.telegram_user)
        guild = update_guild_name("new_name", self.telegram_user)

        self.assertEqual(Guild.objects.count(), 1)
        self.assertEqual(guild.name, "new_name")
        self.assertEqual(guild.captain.telegram_id, self.telegram_user.telegram_id)

    def test_should_update_guild_name_raise_Guild_DoesNotExist_when_invalid_user_is_used(self):
        create_guild(self.guild_name, self.telegram_user)

        with self.assertRaises(Guild.DoesNotExist):
            guild = update_guild_name("new_name", self.telegram_user_2)

    def test_should_create_invite_member_link(self):
        create_guild(self.guild_name, self.telegram_user)
        link = create_invite_member_link(self.telegram_user)

        self.assertEqual(link.guild.name, self.guild_name)

    def test_should_create_invite_member_link_raise_Guild_DoesNotExist_when_invalid_user_is_used(self):
        create_guild(self.guild_name, self.telegram_user)

        with self.assertRaises(Guild.DoesNotExist):
            create_invite_member_link(self.telegram_user_2)

    def test_should_use_invited_id_link(self):
        guild = create_guild(self.guild_name, self.telegram_user)
        link = create_invite_member_link(self.telegram_user)
        use_invited_id_link(self.telegram_user_2, link.link_id)

        self.assertEqual(UserGuild.objects.filter(guild=guild).count(), 2)
        self.assertEqual(InvitationLink.objects.count(), 0)

    def test_should_ignore_invalid_link(self):
        guild = create_guild(self.guild_name, self.telegram_user)
        use_invited_id_link(self.telegram_user_2, str(uuid.uuid4()))

        self.assertEqual(UserGuild.objects.filter(guild=guild).count(), 1)

    # def test_should_(self):
    #     pass
    #
    # def test_should_(self):
    #     pass
