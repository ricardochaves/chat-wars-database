from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
from telegram import ReplyKeyboardRemove
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import CallbackQueryHandler
from telegram.ext import CommandHandler
from telegram.ext import ConversationHandler
from telegram.ext import Dispatcher
from telegram.ext import Filters
from telegram.ext import MessageHandler

from chat_wars_database.app.guild_helper_bot.business.alliance import get_all_chats_for_alliance_atack_orders
from chat_wars_database.app.guild_helper_bot.commands import _get_headquarter_and_build_message
from chat_wars_database.app.guild_helper_bot.commands import _get_locations_and_build_message
from chat_wars_database.app.guild_helper_bot.commands import get_all_hidden_headquarters
from chat_wars_database.app.guild_helper_bot.commands import get_all_hidden_locations
from chat_wars_database.app.guild_helper_bot.decorators import inject_telegram_user
from chat_wars_database.app.guild_helper_bot.models import TelegramUser

FINAL_MESSAGE = """🏆🏆🏆🏆
    
    All members of the alliance, raise their weapons and prepare for our hour!
    
    Let's record our name in the history of this world! We will be the legend!
    
    Pray to the Gods, make your offerings!! 🔱🔱🔱
    
    20 to 40 -> order_20_to_40
    
    41 to 60 -> order_41_to_60
    
    61 to 80 -> order_61_to_80
    
"""

LVL_20_TO_40 = "LVL_20_TO_40"
LVL_41_TO_60 = "LVL_41_TO_60"
LVL_61_80 = "LVL_61_80"
GA_DEF = "GA_DEF"
GA_ATK_LOCATION = "GA_ATK_LOCATION"
GA_DEF_LOCATION = "GA_DEF_LOCATION"
ATK_HEADQUARTER = "ATK_HEADQUARTER"
SHOW_LOCATIONS = "SHOW_LOCATIONS"
SHOW_HEADQUARTERS = "SHOW_HEADQUARTERS"
SEND_MESSAGE = "SEND_MESSAGE"
SELECT_RANGE_LEVEL, SELECT_ORDER, SELECT_LOCATION, SELECT_HEADQUARTER, SELECT_COMBINATION, SEND_MESSAGES = range(6)

MESSAGE = f"""
    
- {LVL_20_TO_40}

- {LVL_41_TO_60}

- {LVL_61_80}
    
    """


def _def_get_message_and_reply_markup_for_select_level(context: CallbackContext):
    message = context.user_data["message"] + "Select level range:"
    keyboard = [
        [
            InlineKeyboardButton("20-40", callback_data=LVL_20_TO_40),
            InlineKeyboardButton("41-60", callback_data=LVL_41_TO_60),
            InlineKeyboardButton("61-80+", callback_data=LVL_61_80),
        ],
        [InlineKeyboardButton("Show final message", callback_data="show_message"),],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    return message, reply_markup


def create_message(update: Update, context: CallbackContext):
    context.user_data["message"] = MESSAGE

    message, reply_markup = _def_get_message_and_reply_markup_for_select_level(context)

    update.message.reply_text(message, reply_markup=reply_markup, one_time_keyboard=True)

    return SELECT_RANGE_LEVEL


def select_level_command(update: Update, context: CallbackContext):

    query = update.callback_query
    text = update.callback_query.data

    bot = context.bot

    context.user_data["lvl"] = text

    message = context.user_data["message"] + f"Select order for {text}"
    keyboard = [
        [InlineKeyboardButton("ga_def", callback_data=GA_DEF),],
        [InlineKeyboardButton("ga_atk location", callback_data=GA_ATK_LOCATION),],
        [InlineKeyboardButton("ga_def location", callback_data=GA_DEF_LOCATION),],
        [InlineKeyboardButton("ga_atk headquarter", callback_data=ATK_HEADQUARTER),],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    bot.edit_message_text(
        chat_id=query.message.chat_id, message_id=query.message.message_id, text=message, reply_markup=reply_markup
    )

    return SELECT_ORDER


@inject_telegram_user
def select_order_command(update: Update, context: CallbackContext, telegram_user: TelegramUser):

    query = update.callback_query
    text = update.callback_query.data
    lvl = context.user_data["lvl"]

    bot = context.bot

    if text == GA_DEF:
        context.user_data["message"] = context.user_data["message"].replace(lvl, f"{lvl} - {text}")
        context.user_data[f"order_{lvl}"] = text
        message, reply_markup = _def_get_message_and_reply_markup_for_select_level(context)
        bot.edit_message_text(
            chat_id=query.message.chat_id, message_id=query.message.message_id, text=message, reply_markup=reply_markup
        )
        return SELECT_RANGE_LEVEL

    if text == GA_ATK_LOCATION:
        all_hidden_locations = get_all_hidden_locations(telegram_user)
        keyboard = []
        for hl in all_hidden_locations:
            keyboard.append(
                [InlineKeyboardButton(f"{hl.name} lvl {hl.lvl}", callback_data=f"ga_atk_{hl.combination}"),]
            )
        reply_markup = InlineKeyboardMarkup(keyboard)
        message = context.user_data["message"] + f"Select the location"
        bot.edit_message_text(
            chat_id=query.message.chat_id, message_id=query.message.message_id, text=message, reply_markup=reply_markup
        )
        return SELECT_COMBINATION

    if text == GA_DEF_LOCATION:
        all_hidden_locations = get_all_hidden_locations(telegram_user)
        keyboard = []
        for hl in all_hidden_locations:
            keyboard.append(
                [InlineKeyboardButton(f"{hl.name} lvl {hl.lvl}", callback_data=f"ga_def_{hl.combination}"),]
            )
        reply_markup = InlineKeyboardMarkup(keyboard)
        message = context.user_data["message"] + f"Select the location"
        bot.edit_message_text(
            chat_id=query.message.chat_id, message_id=query.message.message_id, text=message, reply_markup=reply_markup
        )
        return SELECT_COMBINATION

    if text == ATK_HEADQUARTER:
        all_hidden_headquarters = get_all_hidden_headquarters(telegram_user)
        keyboard = []
        for hq in all_hidden_headquarters:
            keyboard.append(
                [InlineKeyboardButton(f"{hq.name}", callback_data=f"ga_atk_{hq.combination}"),]
            )
        reply_markup = InlineKeyboardMarkup(keyboard)
        message = context.user_data["message"] + f"Select the headquarter"
        bot.edit_message_text(
            chat_id=query.message.chat_id, message_id=query.message.message_id, text=message, reply_markup=reply_markup
        )
        return SELECT_COMBINATION


def select_combination_command(update: Update, context: CallbackContext):
    query = update.callback_query
    text = update.callback_query.data
    lvl = context.user_data["lvl"]

    bot = context.bot

    context.user_data["message"] = context.user_data["message"].replace(lvl, f"{lvl} - {text}")
    context.user_data[f"order_{lvl}"] = text
    message, reply_markup = _def_get_message_and_reply_markup_for_select_level(context)
    bot.edit_message_text(
        chat_id=query.message.chat_id, message_id=query.message.message_id, text=message, reply_markup=reply_markup
    )
    return SELECT_RANGE_LEVEL


def show_final_message_command(update: Update, context: CallbackContext):
    query = update.callback_query
    text = update.callback_query.data

    bot = context.bot

    order_20 = context.user_data["order_" + LVL_20_TO_40]
    order_40 = context.user_data["order_" + LVL_41_TO_60]
    order_60 = context.user_data["order_" + LVL_61_80]
    lvl_20_command = f"{order_20}" if order_20 != GA_DEF else "ga_def"
    lvl_40_command = f"{order_40}" if order_40 != GA_DEF else "ga_def"
    lvl_60_command = f"{order_60}" if order_60 != GA_DEF else "ga_def"

    message = (
        FINAL_MESSAGE.replace("order_20_to_40", lvl_20_command)
        .replace("order_41_to_60", lvl_40_command)
        .replace("order_61_to_80", lvl_60_command)
    )

    keyboard = [
        [
            InlineKeyboardButton("20 to 40", url=f"https://t.me/share/url?url=/" + lvl_20_command),
            InlineKeyboardButton("41 to 60", url=f"https://t.me/share/url?url=/" + lvl_40_command),
            InlineKeyboardButton("61 to 80", url=f"https://t.me/share/url?url=/" + lvl_60_command),
        ],
    ]
    context.user_data["reply_markup"] = InlineKeyboardMarkup(keyboard)

    keyboard.append(
        [InlineKeyboardButton("SEND MESSAGE", callback_data=SEND_MESSAGE),]
    )

    reply_markup = InlineKeyboardMarkup(keyboard)

    context.user_data["message"] = message

    bot.edit_message_text(
        chat_id=query.message.chat_id, message_id=query.message.message_id, text=message, reply_markup=reply_markup
    )
    return SEND_MESSAGES


@inject_telegram_user
def send_messages_in_channels(update: Update, context: CallbackContext, telegram_user: TelegramUser):

    reply_markup = context.user_data["reply_markup"]
    message = context.user_data["message"]

    chats = get_all_chats_for_alliance_atack_orders(telegram_user)
    for c in chats:
        context.bot.send_message(c, message, reply_markup=reply_markup)

    return ConversationHandler.END


def cancel(update: Update, context: CallbackContext):

    update.message.reply_text("Cancelado, execute novamente.", reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def create_new_message_conversation(dp: Dispatcher):
    start_new_char_handler = ConversationHandler(
        entry_points=[CommandHandler("create_message", create_message)],
        states={
            SELECT_RANGE_LEVEL: [
                CallbackQueryHandler(select_level_command, pattern=f"^{LVL_20_TO_40}$"),
                CallbackQueryHandler(select_level_command, pattern=f"^{LVL_41_TO_60}$"),
                CallbackQueryHandler(select_level_command, pattern=f"^{LVL_61_80}$"),
                CallbackQueryHandler(show_final_message_command, pattern=f"show_message"),
            ],
            SELECT_ORDER: [
                CallbackQueryHandler(select_order_command, pattern=f"^{GA_DEF}$"),
                CallbackQueryHandler(select_order_command, pattern=f"^{GA_ATK_LOCATION}$"),
                CallbackQueryHandler(select_order_command, pattern=f"^{GA_DEF_LOCATION}$"),
                CallbackQueryHandler(select_order_command, pattern=f"^{ATK_HEADQUARTER}$"),
            ],
            SELECT_COMBINATION: [
                CallbackQueryHandler(select_combination_command, pattern="ga_atk_.*"),
                CallbackQueryHandler(select_combination_command, pattern="ga_def_.*"),
            ],
            SEND_MESSAGES: [CallbackQueryHandler(send_messages_in_channels, pattern=f"^{SEND_MESSAGE}$")],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    dp.add_handler(start_new_char_handler)
