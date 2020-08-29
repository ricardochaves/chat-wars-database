from django.core.management import BaseCommand

from chat_wars_database.app.guild_helper_bot.models import Guild
from chat_wars_database.app.guild_helper_bot.models import TelegramUser
from chat_wars_database.app.guild_helper_bot.models import UserGuild


class Command(BaseCommand):
    def handle(self, *args, **options):
        t = TelegramUser.objects.create(name="ricardo", user_name="ricardo", telegram_id=123)
        g = Guild.objects.create(name="WAL", captain=t)

        UserGuild.objects.create(user=t, guild=g, role=UserGuild.ADMIN)
