from django.contrib import admin

#
# from chat_wars_database.app.guild_helper_bot.models import Castle
# from chat_wars_database.app.guild_helper_bot.models import Guild
# from chat_wars_database.app.guild_helper_bot.models import GuildMembers
#
#
from chat_wars_database.app.guild_helper_bot.models import Message
from chat_wars_database.app.guild_helper_bot.models import TelegramUser
from chat_wars_database.app.guild_helper_bot.models import UserDeposits


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("message_text",)


@admin.register(UserDeposits)
class GuildMembersAdmin(admin.ModelAdmin):
    pass
