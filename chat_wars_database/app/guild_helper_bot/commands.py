import logging
import re
from datetime import datetime
from datetime import timedelta
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple

from django.db import transaction
from django.db.models import Sum
from django.utils import timezone
from telegram import Update
from telegram.ext import CallbackContext

from chat_wars_database.app.business_core.business import get_or_create_item
from chat_wars_database.app.business_core.models import Item
from chat_wars_database.app.guild_helper_bot.business.guild import get_guild_from_user
from chat_wars_database.app.guild_helper_bot.business.telegram_user import create_telegram_user_if_need
from chat_wars_database.app.guild_helper_bot.decorators import inject_telegram_user
from chat_wars_database.app.guild_helper_bot.decorators import just_for_guild_admin
from chat_wars_database.app.guild_helper_bot.decorators import just_for_private_chat
from chat_wars_database.app.guild_helper_bot.models import Guild
from chat_wars_database.app.guild_helper_bot.models import HiddenHeadquarter
from chat_wars_database.app.guild_helper_bot.models import HiddenLocation
from chat_wars_database.app.guild_helper_bot.models import HiddenMessage
from chat_wars_database.app.guild_helper_bot.models import Message
from chat_wars_database.app.guild_helper_bot.models import TelegramUser
from chat_wars_database.app.guild_helper_bot.models import UserDeposits
from chat_wars_database.app.guild_helper_bot.models import UserGuild

logger = logging.getLogger(__name__)


def help_command(update: Update, context: CallbackContext):  # pylint: disable = unused-argument
    message = """
    Reports:
    /rw - It will take data from the last 7 days.
    /rm - It will take data from the last 30 days.
    /ry - It will take data from the last 365 days.
    
    You can pass the item id or the user to filter the result:
    /rw 13 @ricardobchaves - The total amount of Magic Stones that the user @ricardobchaves deposited in the last week will return.
    
    /week item_id - It will return the total items deposited in the last 7 days grouped by player.
    """
    if update.effective_message.chat.type != "private":
        update.message.reply_markdown(
            "Please [message me privately](http://t.me/ch_guild_helper_bot) for a list of commands."
        )
        return

    update.message.reply_text(message)


def _get_name_and_qtd(message: str) -> Tuple[Optional[str], Optional[int]]:
    regex = "Deposited successfully: (.*) \((\d*)\)"
    m = re.search(regex, message)
    if not m:
        return None, None
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

    if item_name and item_qtd:

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


def _get_combination_from_hidden_location_or_headquarter(message: str) -> str:
    regex = "combination: .*"
    m = re.search(regex, message)
    return m.group(0).replace("combination: ", "")  # type: ignore


def _get_location_data_from_message(message: str) -> Optional[Dict]:
    regex = "(You found hidden location )(.* )(lvl\.\d*)"
    m = re.search(regex, message)
    if not m:
        return None

    data = {
        "name": m.group(2),
        "lvl": int(m.group(3).replace("lvl.", "")),
        "combination": _get_combination_from_hidden_location_or_headquarter(message),
    }

    return data


def _get_headquarter_data_from_message(message: str) -> Optional[Dict]:
    regex = "(You found hidden headquarter )(.*)"
    m = re.search(regex, message)
    if not m:
        return None

    data = {
        "name": m.group(2),
        "combination": _get_combination_from_hidden_location_or_headquarter(message),
    }

    return data


def _execute_found_hidden_location_or_headquarter(telegram_user_data: Dict, message_data: Dict):
    telegram_user, _ = TelegramUser.objects.get_or_create(
        telegram_id=telegram_user_data["telegram_id"], defaults=telegram_user_data
    )

    message_data["telegram_user"] = telegram_user

    if Message.objects.filter(forward_date=message_data["forward_date"], telegram_user=telegram_user).exists():
        logger.info("The message seems repeated, I will ignore")
        return

    location_data = _get_location_data_from_message(message_data["message_text"])
    if location_data:

        if HiddenLocation.objects.filter(combination=location_data["combination"]).exists():
            logger.info("The location already exists, I will ignore")
            return

        with transaction.atomic():
            message = HiddenMessage.objects.create(**message_data)
            hidden_location_data = {
                "telegram_user": telegram_user,
                "message": message,
                "name": location_data["name"],
                "lvl": location_data["lvl"],
                "combination": location_data["combination"],
            }
            HiddenLocation.objects.create(**hidden_location_data)
        return

    headquarter_data = _get_headquarter_data_from_message(message_data["message_text"])
    if headquarter_data:

        if HiddenHeadquarter.objects.filter(combination=headquarter_data["combination"]).exists():
            logger.info("The headquarter already exists, I will ignore")
            return

        with transaction.atomic():
            message = HiddenMessage.objects.create(**message_data)
            hidden_headquarter_data = {
                "telegram_user": telegram_user,
                "message": message,
                "name": headquarter_data["name"],
                "combination": headquarter_data["combination"],
            }
            HiddenHeadquarter.objects.create(**hidden_headquarter_data)
        return


def text_event(update: Update, context: CallbackContext):  # pylint: disable = unused-argument
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
    _execute_found_hidden_location_or_headquarter(telegram_user_data, message_data)


def _build_item_list(deposits, message) -> str:

    deposits = deposits.values("item__name").order_by("item__name").annotate(count=Sum("total"))
    message += "\n"
    for d in deposits:
        message += f"{d['item__name']}: {d['count']}\n"

    return message


def _execute_report(splitted: List[str], guild: Guild) -> str:
    message = ""
    qr = UserDeposits.objects.filter(telegram_user__guild=guild).all()

    if splitted[0] == "/rw":
        dt = timezone.now() - timedelta(days=7)
        qr = qr.filter(message__forward_date__gte=dt)
        message += "What was deposited in the last 7 days.\n"
    if splitted[0] == "/rm":
        dt = timezone.now() - timedelta(days=30)
        qr = qr.filter(message__forward_date__gte=dt)
        message += "What was deposited in the last 30 days.\n"
    if splitted[0] == "/ry":
        dt = timezone.now() - timedelta(days=365)
        qr = qr.filter(message__forward_date__gte=dt)
        message += "What was deposited in the last 365 days.\n"

    if len(splitted) > 1:
        if "@" in splitted[1]:
            user = splitted[1]
            qr = qr.filter(message__telegram_user__name=user)
            message += f"Deposits were made by {user}.\n"
        else:
            item_command = splitted[1]
            qr = qr.filter(item__command__exact=item_command)
            message += f"The report is for the item {item_command}.\n"

    if len(splitted) > 2:
        if "@" in splitted[2]:
            user = splitted[2]
            qr = qr.filter(message__telegram_user__name=user)
            message += f"Deposits were made by {user}.\n"
        else:
            item_command = splitted[2]
            qr = qr.filter(item__command__exact=item_command)
            message += f"The report is for the item {item_command}.\n"

    message = _build_item_list(qr, message)

    return message


@inject_telegram_user
def report_commands(
    update: Update, context: CallbackContext, telegram_user: TelegramUser
):  # pylint: disable = unused-argument

    splited = update.message.text.split(" ")
    user_guild = UserGuild.objects.filter(user=telegram_user).first()
    message = _execute_report(splited, user_guild.guild)
    context.bot.sendMessage(update.message.chat_id, message)
    return


def _execute_week_command(splitted, guild: Guild) -> str:
    dt = timezone.now() - timedelta(days=7)

    item = Item.objects.filter(command=splitted[1]).first()
    deposits = (
        UserDeposits.objects.filter(message__forward_date__gte=dt, item=item, telegram_user__guild=guild)
        .values("telegram_user__name")
        .order_by("telegram_user__name")
        .annotate(count=Sum("total"))
    )

    message = f"Summary of deposits last 7 days: {item.name}\n\n"
    for d in deposits:
        message += f"{d['telegram_user__name'].replace('@', '')}     {d['count']}\n"

    return message


@inject_telegram_user
def week_commands(
    update: Update, context: CallbackContext, telegram_user: TelegramUser
):  # pylint: disable = unused-argument

    splitted = update.message.text.split(" ")
    if len(splitted) == 1:
        context.bot.sendMessage(update.message.chat_id, "You need pass one item id: /week 13")
        return

    user_guild = UserGuild.objects.filter(user=telegram_user).first()
    message = _execute_week_command(splitted, user_guild.guild)
    context.bot.sendMessage(update.message.chat_id, message)


def start_command(update: Update, context: CallbackContext):  # pylint: disable = unused-argument
    if update.effective_message.chat.type != "private":
        update.message.reply_markdown(
            "Please [message me privately](http://t.me/ch_guild_helper_bot) to start at the bot."
        )
        return

    create_telegram_user_if_need(update.effective_user.id, update.effective_user.name, update.effective_user.username)
    help_command(update, context)


@just_for_private_chat
@just_for_guild_admin
@inject_telegram_user
def command_locations(
    update: Update, context: CallbackContext, telegram_user: TelegramUser
):  # pylint: disable = unused-argument

    message = _get_locations_and_build_message(telegram_user)
    update.message.reply_html(message)


def get_all_hidden_locations(telegram_user: TelegramUser) -> List[HiddenLocation]:

    guild_user = UserGuild.objects.get(user=telegram_user)
    guilds = Guild.objects.filter(alliance=guild_user.guild.alliance).all()
    users: List[TelegramUser] = []
    for g in guilds:
        guild_users = UserGuild.objects.filter(guild=g).all()
        for gu in guild_users:
            users.append(gu.user)

    limit_date = datetime.now() - timedelta(days=7)
    all_hidden_location = (
        HiddenLocation.objects.filter(telegram_user__in=users, created_at__gte=limit_date).order_by("-created_at").all()
    )
    return all_hidden_location


def _get_locations_and_build_message(telegram_user: TelegramUser) -> str:
    try:
        all_hidden_location = get_all_hidden_locations(telegram_user)
    except Guild.DoesNotExist:
        return "You dont have alliance"
    except UserGuild.DoesNotExist:
        return "You dont have alliance"
    message = "Locations:\n"
    for hl in all_hidden_location:
        message += f"{hl.name} lvl {hl.lvl} - {hl.combination} - /ga_atk_{hl.combination}\n"

    return message


@just_for_private_chat
@just_for_guild_admin
@inject_telegram_user
def command_headquarter(
    update: Update, context: CallbackContext, telegram_user: TelegramUser
):  # pylint: disable = unused-argument

    message = _get_headquarter_and_build_message(telegram_user)
    update.message.reply_html(message)


def get_all_hidden_headquarters(telegram_user: TelegramUser) -> List[HiddenHeadquarter]:
    guild_user = UserGuild.objects.get(user=telegram_user)
    guilds = Guild.objects.filter(alliance=guild_user.guild.alliance).all()
    users: List[TelegramUser] = []
    for g in guilds:
        guild_users = UserGuild.objects.filter(guild=g).all()
        for gu in guild_users:
            users.append(gu.user)

    all_hidden_headquarter = HiddenHeadquarter.objects.filter(telegram_user__in=users).order_by("-created_at").all()
    return all_hidden_headquarter


def _get_headquarter_and_build_message(telegram_user: TelegramUser) -> str:

    try:
        all_hidden_headquarter = get_all_hidden_headquarters(telegram_user)
    except Guild.DoesNotExist:
        return "You dont have alliance"
    except UserGuild.DoesNotExist:
        return "You dont have alliance"

    message = "Headquarters:\n"
    for hh in all_hidden_headquarter:
        message += f"{hh.name} - {hh.combination} - /ga_atk_{hh.combination}\n"

    return message


def squad_command(update: Update, context: CallbackContext):  # pylint: disable = unused-argument
    if update.effective_message.chat.type != "private":
        return

    guild = get_guild_from_user(update.effective_user.id)
    if not guild:
        update.message.message_text("You dont have a guild")
        return

    update.message.message_text(
        f"""⚜️ Squad ⚜️
{guild.name}
Captain: {guild.captain.name}
Squad link: {guild.link}
"""
    )
