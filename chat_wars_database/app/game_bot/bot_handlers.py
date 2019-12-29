import logging

from telegram import Update
from telegram.ext import CallbackContext

from chat_wars_database.app.business_core.models import Item
from chat_wars_database.app.game_bot.pubsub_service import sent_message
from chat_wars_database.app.setup.help_conn import close_connections

logger = logging.getLogger(__name__)


def graph(update: Update, context: CallbackContext):  # pylint: disable = unused-argument

    text = update.message.text

    data = {
        "chat_id": update.message["chat"]["id"],
        "item_command": text.split("_")[1],
        "graph_time": int(text.split("_")[2]),
    }

    sent_message(data)

    close_connections()

    update.message.reply_text(
        "Your chart will be processed, processing is asynchronous and may take some time depending on the volume of requests queued."  # pylint: disable = line-too-long # noqa
    )


def start(update: Update, context: CallbackContext):  # pylint: disable = unused-argument
    """Send a message when the command /start is issued."""
    update.message.reply_text(
        """
Welcome.
See charts and price trends.
For more information about what I can do and about the project use /help
"""
    )


def help_command(update: Update, context: CallbackContext):  # pylint: disable = unused-argument
    """Send a message when the command /help is issued."""

    message = """
📊 **Graph**

/g\_k83\_25

Where k83 is the Item id and 25 is the total number of days in the chart.
Maximum time allowed is one month

📦 **Item**

/k83

Where k83 is the Item id. Currently all items from Boris and Co, ltd are available.
The next step is to add all Chat Wars items: Stock Exchange Deals

🚧 **About the project**

This project is OpenSource and can be found at [GitHub](https://github.com/ricardochaves/chat-wars-database).
Any contributions are welcome.

It runs on an infrastructure at Gcloud and is funded by @ricardobchaves and the contributors.

Consider making a donation via 💰 [PayPal](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=JL68LZ76ZR3P8&source=url)

Suggestions: [Bot Channel](https://t.me/ricardobotsugestion)
"""  # noqa

    update.message.reply_markdown(message)


def error(update: Update, context: CallbackContext):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def find(update: Update, context: CallbackContext):  # pylint: disable = unused-argument

    if not update.message:
        return

    try:
        term = update.message.text.split(" ")[1]
    except IndexError:
        update.message.reply_markdown("There is something wrong with the command. The correct one is /find recipe")
        return

    items = Item.objects.filter(name__icontains=term, command__isnull=False).all()

    message = ""
    for i in items:
        message += f"\n /{i.command} - {i.name}"

    if message:
        message = (message[:4093] + "...") if len(message) > 4096 else message

        update.message.reply_markdown(message)
    else:
        update.message.reply_markdown("Sorry, I couldn't find anything.")
