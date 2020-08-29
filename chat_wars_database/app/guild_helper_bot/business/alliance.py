from typing import Optional

from chat_wars_database.app.guild_helper_bot.models import Alliance
from chat_wars_database.app.guild_helper_bot.models import TelegramUser
from chat_wars_database.app.guild_helper_bot.models import UserGuild


def alliance_info(telegram_user: TelegramUser) -> Optional[Alliance]:
    guild = UserGuild.objects.get(user=telegram_user).guild
    if guild.alliance:
        return guild.alliance

    return None
