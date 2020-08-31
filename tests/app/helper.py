from chat_wars_database.app.guild_helper_bot.models import Alliance
from chat_wars_database.app.guild_helper_bot.models import Guild
from chat_wars_database.app.guild_helper_bot.models import GuildChannel
from chat_wars_database.app.guild_helper_bot.models import TelegramUser
from chat_wars_database.app.guild_helper_bot.models import UserGuild


def create_alliance(name: str, guild: Guild) -> Alliance:
    return Alliance.objects.create(name=name, owner=guild)


def add_guild_to_alliance(guild: Guild, alliance: Alliance) -> None:
    guild.alliance = alliance
    guild.save()


def create_guild(name: str, captain: TelegramUser) -> Guild:
    return Guild.objects.create(name=name, captain=captain)


def create_telegram_user(name: str, user_name: str, telegram_id: int) -> TelegramUser:
    return TelegramUser.objects.create(name=name, user_name=user_name, telegram_id=telegram_id)


def create_user_guild(user: TelegramUser, guild: Guild, role: int) -> UserGuild:
    return UserGuild.objects.create(user=user, guild=guild, role=role)


def create_guild_channel(chat_id: int, name: str, alliance_atack_orders: bool, guild: Guild) -> GuildChannel:
    return GuildChannel.objects.create(
        chat_id=chat_id, name=name, alliance_atack_orders=alliance_atack_orders, guild=guild
    )
