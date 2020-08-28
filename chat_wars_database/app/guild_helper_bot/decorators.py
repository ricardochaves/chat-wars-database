import logging
from functools import wraps

from django import db
from telegram import Update
from telegram.ext import CallbackContext

from chat_wars_database.app.guild_helper_bot.business.telegram_user import create_telegram_user_if_need
from chat_wars_database.app.helper import make_sure_connection_usable
from chat_wars_database.settings import BOT_CLOSE_CONNECTIONS


def just_for_group_chat(func):
    @wraps(func)
    def wrapped(update: Update, context: CallbackContext, *args, **kwargs):

        if update.effective_message.chat.type != "group":
            return

        result = func(update, context, *args, **kwargs)
        return result

    return wrapped


def just_for_private_chat(func):
    @wraps(func)
    def wrapped(update: Update, context: CallbackContext, *args, **kwargs):

        if update.effective_message.chat.type != "private":
            return

        result = func(update, context, *args, **kwargs)
        return result

    return wrapped


def inject_telegram_user(func):
    @wraps(func)
    def wrapped(update: Update, context: CallbackContext, *args, **kwargs):

        make_sure_connection_usable()

        # user_id = update.effective_user.id
        # char = Character.objects.filter(player__telegram_id=user_id).first()

        telegram_user = create_telegram_user_if_need(
            update.effective_user.id, update.effective_user.id, update.effective_user.id
        )

        # if not char:
        #     update.message.reply_text(NO_CHAR_FOUND)
        #     return

        # context.user_data["telegram_user"] = telegram_user
        result = func(update, context, telegram_user, *args, **kwargs)

        if BOT_CLOSE_CONNECTIONS:
            db.connections.close_all()

        return result

    return wrapped
