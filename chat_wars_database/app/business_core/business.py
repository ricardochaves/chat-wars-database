import logging
import re

from telegram import Update
from telegram.ext import CallbackContext

from chat_wars_database.app.business_auction.lot_details import get_item_lot_details
from chat_wars_database.app.business_core.message_builders import build_item_message_auction
from chat_wars_database.app.business_core.message_builders import build_item_message_exchange
from chat_wars_database.app.business_core.models import Item
from chat_wars_database.app.business_exchange.business import get_exchange_data

logger = logging.getLogger(__name__)


def build_message(item: Item) -> str:
    message = ""

    if item.tradeable_auction:
        lots_data = get_item_lot_details(item)
        logger.info("Data received")
        if lots_data:
            message = build_item_message_auction(lots_data, item)

    if item.tradeable_exchange:
        exchange_data = get_exchange_data(item)
        if exchange_data:
            message = build_item_message_exchange(exchange_data, item)

    if not message:
        message = "Item not found"
    return message


def get_or_create_item(name: str) -> Item:

    item = Item.objects.filter(name=name).first()

    if not item:
        item = Item.objects.create(name=name)
        item.save()

    return item


def cleaner_item_name(name: str) -> str:
    name = re.sub(r"\+\d+⚔", "", name)
    name = re.sub(r"\+\d+🛡", "", name)
    name = re.sub(r"\+\d+💧", "", name)
    return re.sub(r"⚡\+\d+", "", name).replace(" ️", "").strip()


def route_command(update: Update, context: CallbackContext) -> None:  # pylint: disable = unused-argument
    text = update.message["text"]
    logger.info("New command to route: %s", text)

    item = Item.objects.filter(command=text.replace("/", "")).first()

    if item:
        logger.info("Item found: %s", item.name)

        message = build_message(item)

        logger.info("Message: %s", message)

        update.message.reply_markdown(message)
        return

    update.message.reply_markdown("Sorry. Item not found.")
