from django.contrib import admin

#
# from chat_wars_database.app.guild_helper_bot.models import Castle
# from chat_wars_database.app.guild_helper_bot.models import Guild
# from chat_wars_database.app.guild_helper_bot.models import GuildMembers
#
#
from chat_wars_database.app.guild_helper_bot.models import Alliance
from chat_wars_database.app.guild_helper_bot.models import Guild
from chat_wars_database.app.guild_helper_bot.models import InvitationLink
from chat_wars_database.app.guild_helper_bot.models import Message
from chat_wars_database.app.guild_helper_bot.models import TelegramUser
from chat_wars_database.app.guild_helper_bot.models import UserDeposits
from chat_wars_database.app.guild_helper_bot.models import UserGuild


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("message_text",)


@admin.register(UserDeposits)
class GuildMembersAdmin(admin.ModelAdmin):
    pass


@admin.register(Guild)
class GuildAdmin(admin.ModelAdmin):
    pass


@admin.register(UserGuild)
class UserGuildAdmin(admin.ModelAdmin):
    pass


@admin.register(InvitationLink)
class InvitationLinkAdmin(admin.ModelAdmin):
    pass


@admin.register(Alliance)
class AllianceAdmin(admin.ModelAdmin):
    pass
