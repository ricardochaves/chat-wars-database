import logging

from django.core.management import BaseCommand
from telegram.ext import CommandHandler
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import RegexHandler
from telegram.ext import Updater

from chat_wars_database.app.game_bot.bot_handlers import error
from chat_wars_database.app.game_bot.bot_handlers import under_maintenance
from chat_wars_database.app.guild_helper_bot.business.commands import telegram_command_alliance_info
from chat_wars_database.app.guild_helper_bot.business.commands import telegram_command_create_guild
from chat_wars_database.app.guild_helper_bot.business.commands import telegram_command_create_invite_member_link
from chat_wars_database.app.guild_helper_bot.business.commands import telegram_command_guild_info
from chat_wars_database.app.guild_helper_bot.business.commands import telegram_command_leave_guild
from chat_wars_database.app.guild_helper_bot.business.commands import telegram_command_update_guild_name
from chat_wars_database.app.guild_helper_bot.business.commands import telegram_command_use_invited_id_link
from chat_wars_database.app.guild_helper_bot.business.commands import telegram_command_use_leave_guild
from chat_wars_database.app.guild_helper_bot.commands import command_headquarter
from chat_wars_database.app.guild_helper_bot.commands import command_locations
from chat_wars_database.app.guild_helper_bot.commands import help_command
from chat_wars_database.app.guild_helper_bot.commands import report_commands
from chat_wars_database.app.guild_helper_bot.commands import squad_command
from chat_wars_database.app.guild_helper_bot.commands import start_command
from chat_wars_database.app.guild_helper_bot.commands import text_event
from chat_wars_database.app.guild_helper_bot.commands import week_commands
from chat_wars_database.settings import TELEGRAM_GAME_BOT_TOKEN
from chat_wars_database.settings import UNDER_MAINTENANCE

logger = logging.getLogger(__name__)


def add_handlers(dp):
    if UNDER_MAINTENANCE:
        dp.add_handler(MessageHandler(Filters.all, under_maintenance))
        return

    dp.add_handler(CommandHandler("rw", report_commands))
    dp.add_handler(CommandHandler("rm", report_commands))
    dp.add_handler(CommandHandler("ry", report_commands))
    dp.add_handler(CommandHandler("week", week_commands))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CommandHandler("create_guild", telegram_command_create_guild))
    dp.add_handler(CommandHandler("leave_guild", telegram_command_leave_guild))
    dp.add_handler(CommandHandler("update_guild_name", telegram_command_update_guild_name))
    dp.add_handler(CommandHandler("create_invite_member_link", telegram_command_create_invite_member_link))
    dp.add_handler(CommandHandler("guild_info", telegram_command_guild_info))
    dp.add_handler(CommandHandler("alliance_info", telegram_command_alliance_info))
    dp.add_handler(CommandHandler("locations", command_locations))
    dp.add_handler(CommandHandler("headquarters", command_headquarter))

    dp.add_handler(RegexHandler("use_link_.*", telegram_command_use_invited_id_link))
    dp.add_handler(RegexHandler("leave_guild_\d*", telegram_command_use_leave_guild))
    # dp.add_handler(MessageHandler("⚜️Squad", squad_command))
    dp.add_handler(MessageHandler(Filters.text, text_event))


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TELEGRAM_GAME_BOT_TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    add_handlers(dp)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    logger.info("Listening...")
    updater.idle()


class Command(BaseCommand):
    def handle(self, *args, **options):
        main()


main()
