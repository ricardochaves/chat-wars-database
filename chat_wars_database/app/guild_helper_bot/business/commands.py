from django.db import IntegrityError
from telegram import Update
from telegram.ext import CallbackContext

from chat_wars_database.app.guild_helper_bot.business.alliance import alliance_info
from chat_wars_database.app.guild_helper_bot.business.guild import create_guild
from chat_wars_database.app.guild_helper_bot.business.guild import create_invite_member_link
from chat_wars_database.app.guild_helper_bot.business.guild import guild_info
from chat_wars_database.app.guild_helper_bot.business.guild import leave_guild
from chat_wars_database.app.guild_helper_bot.business.guild import update_guild_name
from chat_wars_database.app.guild_helper_bot.business.guild import use_guild_leave_code
from chat_wars_database.app.guild_helper_bot.business.guild import use_invited_id_link
from chat_wars_database.app.guild_helper_bot.decorators import inject_telegram_user
from chat_wars_database.app.guild_helper_bot.decorators import just_for_private_chat
from chat_wars_database.app.guild_helper_bot.exceptions import CaptainCantLeaveTheGuild
from chat_wars_database.app.guild_helper_bot.models import Alliance
from chat_wars_database.app.guild_helper_bot.models import Guild
from chat_wars_database.app.guild_helper_bot.models import TelegramUser
from chat_wars_database.app.guild_helper_bot.models import UserGuild


@just_for_private_chat
@inject_telegram_user
def telegram_command_create_guild(update: Update, context: CallbackContext, telegram_user: TelegramUser):
    split_command = update.effective_message.text.split(" ")
    if len(split_command) < 2:
        update.message.reply_html("Invalid command, use /create_guild guild_name")
        return

    split_command.pop(0)
    guild_name = "".join(split_command)
    message = command_create_guild(guild_name, telegram_user)
    update.message.reply_html(message)


@just_for_private_chat
@inject_telegram_user
def telegram_command_leave_guild(update: Update, context: CallbackContext, telegram_user: TelegramUser):
    message = command_leave_guild(telegram_user)
    update.message.reply_html(message)


@just_for_private_chat
@inject_telegram_user
def telegram_command_use_leave_guild(update: Update, context: CallbackContext, telegram_user: TelegramUser):
    message = command_use_leave_guild(telegram_user, update.effective_message.text.replace("/", ""))
    update.message.reply_html(message)


@just_for_private_chat
@inject_telegram_user
def telegram_command_update_guild_name(update: Update, context: CallbackContext, telegram_user: TelegramUser):
    split_command = update.effective_message.text.split(" ")
    if len(split_command) < 2:
        update.message.reply_html("Invalid command, use /update_guild_name new_guild_name")
        return

    split_command.pop(0)
    guild_name = "".join(split_command)

    message = command_update_guild_name(guild_name, telegram_user)
    update.message.reply_html(message)


@just_for_private_chat
@inject_telegram_user
def telegram_command_create_invite_member_link(update: Update, context: CallbackContext, telegram_user: TelegramUser):
    message = command_create_invite_member_link(telegram_user)
    update.message.reply_html(message)


@just_for_private_chat
@inject_telegram_user
def telegram_command_use_invited_id_link(update: Update, context: CallbackContext, telegram_user: TelegramUser):
    split_command = update.effective_message.text.split("_")
    if len(split_command) < 3:
        update.message.reply_html("Invalid command")
        return

    link = split_command[2]
    message = command_use_invited_id_link(telegram_user, link)
    update.message.reply_html(message)


@just_for_private_chat
@inject_telegram_user
def telegram_command_guild_info(update: Update, context: CallbackContext, telegram_user: TelegramUser):
    message = command_guild_info(telegram_user)
    update.message.reply_html(message)


def command_guild_info(telegram_user: TelegramUser) -> str:
    try:
        guild = guild_info(telegram_user)
        users = guild.userguild_set.all()
        user_list = ""
        for u in users:
            user_list += f"{u.user.name}\n"

        return f"""Guild: {guild.name}

{user_list}

To leave the guild use /leave_guild
"""
    except UserGuild.DoesNotExist:
        return f"You don't have any guild"


def command_use_invited_id_link(telegram_user: TelegramUser, link: str) -> str:

    use_invited_id_link(telegram_user, link)
    return "Bem vindo a guild, use /guild_info"


def command_leave_guild(telegram_user: TelegramUser):
    try:
        command = leave_guild(telegram_user)
        return f"To confirm your exit use /{command}"
    except UserGuild.DoesNotExist:
        return f"You don't have any guild"


def command_use_leave_guild(telegram_user: TelegramUser, leave_command: str) -> str:
    try:
        use_guild_leave_code(telegram_user, leave_command)
        return f"You leaved the guild"
    except UserGuild.DoesNotExist:
        return f"You don't have any guild"
    except CaptainCantLeaveTheGuild:
        return "The captain cannot leave the guild, elect another captain or delete the guild"


def command_create_guild(guild_name: str, telegram_user: TelegramUser) -> str:
    try:
        create_guild(guild_name, telegram_user)
        return f"""Guild {guild_name} created

Use /create_invite_member_link to create an invitation link to send to guild members."""
    except IntegrityError:
        return f"The name {guild_name} already in use or you already have a guild"


def command_update_guild_name(new_guild_name: str, telegram_user: TelegramUser) -> str:
    try:
        update_guild_name(new_guild_name, telegram_user)
        return "Guild name updated"
    except Guild.DoesNotExist:
        return f"You don't have any guild. Use /create_guild <name>"


def command_create_invite_member_link(telegram_user: TelegramUser) -> str:

    link = create_invite_member_link(telegram_user)
    return f"""{telegram_user.name}  is inviting you to the guild {telegram_user.guild.name}.
Send this link /use_link_{link.link_id} message to @ch_guild_helper_bot to join the guild"""


@just_for_private_chat
@inject_telegram_user
def telegram_command_alliance_info(update: Update, context: CallbackContext, telegram_user: TelegramUser):
    message = command_alliance_info(telegram_user)
    update.message.reply_html(message)


def command_alliance_info(telegram_user: TelegramUser) -> str:

    try:
        alliance = alliance_info(telegram_user)
        if not alliance:
            return "Your guild does not have an alliance"

        guilds_count = alliance.guild_set.count()
        guilds = alliance.guild_set.all()
        total_members = 0
        for g in guilds:
            total_members += g.userguild_set.count()

        return f"""{alliance.name}
Guilds: {guilds_count} 👥 {total_members}
Owner: {alliance.owner}"""

    except UserGuild.DoesNotExist:
        return f"You don't have any guild. Use /create_guild <name>"
