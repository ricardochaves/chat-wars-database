import logging
import os

import requests

from chat_wars_database.settings import TELEGRAM_GAME_BOT_TOKEN

logger = logging.getLogger(__name__)

TELEGRAM_POST_PHOTO_URL = f"https://api.telegram.org/bot{TELEGRAM_GAME_BOT_TOKEN}/sendPhoto"
TELEGRAM_POST_MESSAGE_URL = f"https://api.telegram.org/bot{TELEGRAM_GAME_BOT_TOKEN}/sendMessage"


def send_photo(message: str, image: str, user_id: str) -> None:

    with open(image, "rb") as file:

        multipart_form_data = {"photo": ("graph.png", file), "chat_id": (None, user_id), "caption": (None, message)}

        requests.post(url=TELEGRAM_POST_PHOTO_URL, files=multipart_form_data)

    os.remove(image)


def send_message(message: str, user_id: str) -> None:
    logger.info("Send message by POST")

    data = {"parse_mode": "HTML", "chat_id": user_id, "text": message}

    requests.post(url=TELEGRAM_POST_MESSAGE_URL, json=data)
