from django.contrib import admin

#
# from chat_wars_database.app.guild_helper_bot.models import Castle
# from chat_wars_database.app.guild_helper_bot.models import Guild
# from chat_wars_database.app.guild_helper_bot.models import GuildMembers
#
#
from chat_wars_database.app.guild_helper_bot.models import Alliance
from chat_wars_database.app.guild_helper_bot.models import Guild
from chat_wars_database.app.guild_helper_bot.models import GuildChannel
from chat_wars_database.app.guild_helper_bot.models import HiddenHeadquarter
from chat_wars_database.app.guild_helper_bot.models import HiddenLocation
from chat_wars_database.app.guild_helper_bot.models import HiddenMessage
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


@admin.register(HiddenMessage)
class HiddenMessageAdmin(admin.ModelAdmin):
    list_display = ("created_at", "telegram_user", "_hidden_location", "_hidden_headquarter")

    @staticmethod
    def _hidden_location(obj):
        location = obj.hiddenlocation_set.first()
        if location:
            return f"{location.name} - {location.lvl} - {location.combination}"

    @staticmethod
    def _hidden_headquarter(obj):
        headquarter = obj.hiddenheadquarter_set.first()
        if headquarter:
            return f"{headquarter.name} - {headquarter.combination}"


@admin.register(HiddenLocation)
class HiddenLocationAdmin(admin.ModelAdmin):
    list_display = ("created_at", "telegram_user", "name", "lvl", "combination")


@admin.register(HiddenHeadquarter)
class HiddenHeadquarterAdmin(admin.ModelAdmin):
    list_display = ("created_at", "telegram_user", "name", "combination")


@admin.register(GuildChannel)
class GuildChannelAdmin(admin.ModelAdmin):
    pass
