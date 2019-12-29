import json
from typing import Dict

from google.cloud import pubsub_v1

from chat_wars_database.settings import GOOGLE_CLOUD_BOT_TOPIC_NAME
from chat_wars_database.settings import GOOGLE_CLOUD_PROJECT

publisher = pubsub_v1.PublisherClient()
topic_name = f"projects/{GOOGLE_CLOUD_PROJECT}/topics/{GOOGLE_CLOUD_BOT_TOPIC_NAME}"


def sent_message(message: Dict) -> None:

    publisher.publish(topic_name, json.dumps(message).encode("utf-8"))
