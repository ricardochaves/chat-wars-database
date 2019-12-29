import json
import logging

from django.core.management import BaseCommand
from django.db import transaction
from google.cloud import pubsub_v1

from chat_wars_database.app.game_bot.create_graph import create_graph
from chat_wars_database.app.game_bot.telegram_service import send_message
from chat_wars_database.settings import GOOGLE_CLOUD_BOT_SUBSCRIPTION_NAME
from chat_wars_database.settings import GOOGLE_CLOUD_PROJECT

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
        logger.info("start command")

        subscriber = pubsub_v1.SubscriberClient()
        subscription_name = f"projects/{GOOGLE_CLOUD_PROJECT}/subscriptions/{GOOGLE_CLOUD_BOT_SUBSCRIPTION_NAME}"

        def callback(message):
            logger.info("Message received: %s", message)

            try:

                data = json.loads(message.data.decode("utf-8").replace("'", '"'))

            except BaseException as e:
                logger.info(message.data)
                logger.warning("Error: %s", e)
                message.ack()
                return

            with transaction.atomic():
                try:
                    create_graph(data)
                except BaseException:
                    logger.exception("Error create_graph")
                    send_message(
                        "I cant create your graph now, Send this to @ricardobchaves to let him know and fix the error.",
                        message["chat_id"],
                    )
                finally:
                    message.ack()

        flow_control = pubsub_v1.types.FlowControl(max_messages=2, max_bytes=10000, max_lease_duration=20)

        future = subscriber.subscribe(subscription_name, callback=callback, flow_control=flow_control)

        try:
            logger.info("loop future now...")
            future.result()
        except BaseException:
            logger.exception("future.result")
            raise
