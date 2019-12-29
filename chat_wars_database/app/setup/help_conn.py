from django import db

from chat_wars_database.settings import COMMAND_CLOSE_CONNECTIONS


def close_connections() -> None:

    if COMMAND_CLOSE_CONNECTIONS:
        db.connections.close_all()
