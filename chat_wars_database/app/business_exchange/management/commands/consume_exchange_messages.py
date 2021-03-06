import asyncio
import logging
import os
from datetime import timedelta

from django.core.management import BaseCommand
from django.db import IntegrityError
from django.utils import timezone
from telethon import TelegramClient
from telethon.sessions import StringSession

from chat_wars_database.app.business_exchange.models import ExchangeMessages
from chat_wars_database.settings import TELEGRAM_API_HASH
from chat_wars_database.settings import TELEGRAM_API_ID
from chat_wars_database.settings import TELEGRAM_CELL_PHONE
from chat_wars_database.settings import TELEGRAM_STRING

logger = logging.getLogger(__name__)

client = TelegramClient(StringSession(TELEGRAM_STRING), TELEGRAM_API_ID, TELEGRAM_API_HASH)
client.start(phone=TELEGRAM_CELL_PHONE)

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"


async def main(total_days: int):
    logger.info("Start")
    async with client:

        logger.info("Client")

        async for m in client.iter_messages("chtwrsExchange"):
            logger.info("id: %s, date: %s", m.id, m.date)

            if total_days > 0:
                if m.date < timezone.now() - timedelta(days=total_days):
                    logger.info("Braking now")
                    break
            try:
                ExchangeMessages.objects.create(message_id=m.id, message_date=m.date, message_text=m.message)
            except IntegrityError:
                continue


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("total_days", type=int)

    def handle(self, *args, **options):

        loop = asyncio.get_event_loop()
        loop.run_until_complete(main(options["total_days"]))

        try:
            client.disconnect()
        except BaseException as e:
            logger.debug(e)

        logger.info("done")
