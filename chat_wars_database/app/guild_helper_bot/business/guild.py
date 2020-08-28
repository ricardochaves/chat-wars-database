from datetime import datetime
from typing import Optional

from django.db import transaction

from chat_wars_database.app.guild_helper_bot.exceptions import CaptainCantLeaveTheGuild
from chat_wars_database.app.guild_helper_bot.models import Guild
from chat_wars_database.app.guild_helper_bot.models import InvitationLink
from chat_wars_database.app.guild_helper_bot.models import TelegramUser
from chat_wars_database.app.guild_helper_bot.models import UserGuild


def create_guild(guild_name: str, telegram_user: TelegramUser) -> Guild:
    guild = Guild.objects.create(name=guild_name, captain=telegram_user)
    UserGuild.objects.create(user=telegram_user, guild=guild, role=UserGuild.ADMIN)
    return guild


def delete_guild(telegram_user: TelegramUser) -> Guild:
    return Guild.objects.filter(captain=telegram_user).delete()


def update_guild_name(new_guild_name: str, telegram_user: TelegramUser) -> Guild:
    guild = Guild.objects.get(captain=telegram_user)

    guild.name = new_guild_name
    guild.save()

    return guild


def create_invite_member_link(telegram_user: TelegramUser) -> InvitationLink:
    guild = Guild.objects.get(captain=telegram_user)

    return InvitationLink.objects.create(guild=guild)


def add_new_admin(telegram_user: TelegramUser) -> None:
    pass


def use_invited_id_link(telegram_user: TelegramUser, invited_link: str) -> None:
    link = InvitationLink.objects.filter(link_id=invited_link).first()

    if link:
        with transaction.atomic():
            link.delete()
            UserGuild.objects.create(user=telegram_user, guild=link.guild, role=UserGuild.MEMBER)


def get_guild_from_user(telegram_id: int) -> Optional[Guild]:
    return Guild.objects.filter(userguild__user__telegram_id=telegram_id).first()


def leave_guild(telegram_user: TelegramUser) -> str:
    user_guild = UserGuild.objects.get(user=telegram_user)
    user_guild.leave_command = f"leave_guild_{int(datetime.now().timestamp())}"
    user_guild.save()
    return user_guild.leave_command


def use_guild_leave_code(telegram_user: TelegramUser, leave_command: str) -> None:
    with transaction.atomic():
        guild = Guild.objects.filter(captain=telegram_user).first()
        if guild:
            raise CaptainCantLeaveTheGuild()

        UserGuild.objects.get(user=telegram_user, leave_command=leave_command).delete()


def guild_info(telegram_user: TelegramUser) -> Guild:
    return UserGuild.objects.get(user=telegram_user).guild
