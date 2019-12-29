import logging

from django.core.management import BaseCommand
from telegram.ext import CommandHandler
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import Updater

from chat_wars_database.app.business_core.business import route_command
from chat_wars_database.app.game_bot.bot_handlers import error
from chat_wars_database.app.game_bot.bot_handlers import graph
from chat_wars_database.app.game_bot.bot_handlers import help_command
from chat_wars_database.app.game_bot.bot_handlers import start
from chat_wars_database.settings import TELEGRAM_GAME_BOT_TOKEN

logger = logging.getLogger(__name__)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TELEGRAM_GAME_BOT_TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.regex("\/g_.*?(?=_)_([1-2]\d$|[0-9]$)"), graph))
    dp.add_handler(MessageHandler(Filters.command, route_command))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


class Command(BaseCommand):
    def handle(self, *args, **options):
        main()