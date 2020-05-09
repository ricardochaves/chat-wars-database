import logging

from django.core.management import BaseCommand
from telegram.ext import CommandHandler
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import Updater

from chat_wars_database.app.game_bot.bot_handlers import error
from chat_wars_database.app.game_bot.bot_handlers import under_maintenance
from chat_wars_database.app.guild_helper_bot.commands import deposit_event
from chat_wars_database.app.guild_helper_bot.commands import report_commands
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

    dp.add_handler(MessageHandler(Filters.text, deposit_event))


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
