from typing import List
from typing import Optional

from chat_wars_database.app.guild_helper_bot.models import Alliance
from chat_wars_database.app.guild_helper_bot.models import Guild
from chat_wars_database.app.guild_helper_bot.models import GuildChannel
from chat_wars_database.app.guild_helper_bot.models import HiddenHeadquarter
from chat_wars_database.app.guild_helper_bot.models import HiddenLocation
from chat_wars_database.app.guild_helper_bot.models import TelegramUser
from chat_wars_database.app.guild_helper_bot.models import UserGuild


def alliance_info(telegram_user: TelegramUser) -> Optional[Alliance]:
    guild = UserGuild.objects.get(user=telegram_user).guild
    if guild.alliance:
        return guild.alliance

    return None


def get_target_infos(target: str) -> str:

    location = HiddenLocation.objects.filter(combination=target).first()

    if location:
        return f"{location.name} - {location.lvl}"

    headquarter = HiddenHeadquarter.objects.filter(combination=target).first()

    if headquarter:
        return f"{headquarter.name}"

    return ""


def get_all_chats_for_alliance_atack_orders(telegram_user: TelegramUser) -> List[int]:

    user_guild = UserGuild.objects.get(user=telegram_user)
    if not user_guild.guild.alliance:
        return []

    guilds_from_alliance = Guild.objects.filter(alliance=user_guild.guild.alliance).all()

    list_chat: List[int] = []
    for g in guilds_from_alliance:
        channels = GuildChannel.objects.filter(guild=g, alliance_atack_orders=True).all()
        for c in channels:
            list_chat.append(c.chat_id)

    return list_chat
