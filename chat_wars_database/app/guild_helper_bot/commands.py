import logging
import re
from datetime import timedelta
from typing import Dict
from typing import List
from typing import Tuple

from django.db import transaction
from django.db.models import Sum
from django.utils import timezone
from telegram import Update
from telegram.ext import CallbackContext

from chat_wars_database.app.business_core.business import get_or_create_item
from chat_wars_database.app.business_core.models import Item
from chat_wars_database.app.guild_helper_bot.models import Message
from chat_wars_database.app.guild_helper_bot.models import TelegramUser
from chat_wars_database.app.guild_helper_bot.models import UserDeposits

logger = logging.getLogger(__name__)


def help_command(update: Update, context: CallbackContext):  # pylint: disable = unused-argument
    message = """
    Reports:
    /rw - It will take data from the last 7 days.
    /rm - It will take data from the last 30 days.
    /ry - It will take data from the last 365 days.
    
    You can pass the item id or the user to filter the result:
    /rw 13 @ricardobchaves - The total amount of Magic Stones that the user @ricardobchaves deposited in the last week will return.
    """
    update.message.reply_markdown(message)


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
        logger.info("The message seems repeated, I will ignore")
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

    logger.info("Deposit successfully executed.")


def deposit_event(update: Update, context: CallbackContext):  # pylint: disable = unused-argument
    if not update.message.forward_from:
        logging.info("Message is not forwarded")
        return
    if not update.message.forward_from.username == "chtwrsbot":
        logging.info("Message is not forwarded from bot chtwrsbot")
        return

    logger.info("Message sent correctly. Executing deposit.")
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


def _build_item_list(deposits, message) -> str:

    deposits = deposits.values("item__name").order_by("item__name").annotate(count=Sum("total"))
    message += "\n"
    for d in deposits:
        message += f"{d['item__name']}: {d['count']}\n"

    return message


def _execute_report(splited: List[str]) -> str:
    message = ""
    qr = UserDeposits.objects.all()

    if splited[0] == "/rw":
        dt = timezone.now() - timedelta(days=7)
        qr = qr.filter(message__forward_date__gte=dt)
        message += "What was deposited in the last 7 days.\n"
    if splited[0] == "/rm":
        dt = timezone.now() - timedelta(days=30)
        qr = qr.filter(message__forward_date__gte=dt)
        message += "What was deposited in the last 30 days.\n"
    if splited[0] == "/ry":
        dt = timezone.now() - timedelta(days=365)
        qr = qr.filter(message__forward_date__gte=dt)
        message += "What was deposited in the last 365 days.\n"

    if len(splited) > 1:
        if "@" in splited[1]:
            user = splited[1]
            qr = qr.filter(message__telegram_user__name=user)
            message += f"Deposits were made by {user}.\n"
        else:
            item_command = splited[1]
            qr = qr.filter(item__command__exact=item_command)
            message += f"The report is for the item {item_command}.\n"

    if len(splited) > 2:
        if "@" in splited[2]:
            user = splited[2]
            qr = qr.filter(message__telegram_user__name=user)
            message += f"Deposits were made by {user}.\n"
        else:
            item_command = splited[2]
            qr = qr.filter(item__command__exact=item_command)
            message += f"The report is for the item {item_command}.\n"

    message = _build_item_list(qr, message)

    return message


def report_commands(update: Update, context: CallbackContext):  # pylint: disable = unused-argument

    splited = update.message.text.split(" ")
    message = _execute_report(splited)
    context.bot.sendMessage(update.message.chat_id, message)
    return


def _execute_week_command(splited) -> str:
    dt = timezone.now() - timedelta(days=7)

    item = Item.objects.filter(command=splited[1]).first()
    deposits = (
        UserDeposits.objects.filter(message__forward_date__gte=dt, item=item)
        .values("telegram_user__name")
        .order_by("telegram_user__name")
        .annotate(count=Sum("total"))
    )

    message = f"Summary of deposits last 7 days: {item.name}\n\n"
    for d in deposits:
        message += f"{d['telegram_user__name'].replace('@', '')}     {d['count']}"

    return message


def week_commands(update: Update, context: CallbackContext):  # pylint: disable = unused-argument

    splited = update.message.text.split(" ")
    if len(splited) == 1:
        context.bot.sendMessage(update.message.chat_id, "You need pass one item id: /week 13")
        return

    message = _execute_week_command(splited)
    context.bot.sendMessage(update.message.chat_id, message)
