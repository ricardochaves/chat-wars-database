import logging
import re
from typing import Dict
from typing import Tuple

from django.db import transaction
from telegram import Update
from telegram.ext import CallbackContext

from chat_wars_database.app.business_core.business import get_or_create_item
from chat_wars_database.app.business_core.models import Item
from chat_wars_database.app.guild_helper_bot.models import Message
from chat_wars_database.app.guild_helper_bot.models import TelegramUser
from chat_wars_database.app.guild_helper_bot.models import UserDeposits


def _get_name_and_qtd(message: str) -> Tuple[str, int]:
    regex = "Deposited successfully: (.*) \((\d)\)"
    m = re.search(regex, message)
    item_name = m.group(1)  # type: ignore
    item_qtd = int(m.group(2))  # type: ignore

    return item_name, item_qtd


def _execute_deposit(telegram_user_data: Dict, message_data: Dict) -> None:

    telegram_user, _ = TelegramUser.objects.get_or_create(
        telegram_id=telegram_user_data["telegram_id"], defaults=telegram_user_data
    )

    message_data["telegram_user"] = telegram_user

    if Message.objects.filter(forward_date=message_data["forward_date"], telegram_user=telegram_user).exists():
        return

    item_name, item_qtd = _get_name_and_qtd(message_data["message_text"])
    item = get_or_create_item(item_name)

    with transaction.atomic():
        message = Message.objects.create(**message_data)

        user_deposits_data = {
            "telegram_user": telegram_user,
            "message": message,
            "item": item,
            "total": item_qtd,
        }

        UserDeposits.objects.create(**user_deposits_data)


def deposit_event(update: Update, context: CallbackContext):  # pylint: disable = unused-argument
    if not update.message.forward_from:
        return
    if not update.message.forward_from.username == "chtwrsbot":
        return

    telegram_user_data = {
        "user_name": update.effective_user.username,
        "name": update.effective_user.name,
        "telegram_id": update.effective_user.id,
    }

    message_data = {
        "chat_id": update.message.chat_id,
        "forward_date": update.message.forward_date,
        "message_text": update.message.text,
        "message_id": update.message.message_id,
    }

    _execute_deposit(telegram_user_data, message_data)


# update.message.forward_date
# update.message.forward_from.username = 'chtwrsbot'
