from django.test import TestCase
from django.utils import timezone

from chat_wars_database.app.business_core.models import Item
from chat_wars_database.app.guild_helper_bot.commands import _execute_deposit
from chat_wars_database.app.guild_helper_bot.commands import _execute_report
from chat_wars_database.app.guild_helper_bot.models import Guild
from chat_wars_database.app.guild_helper_bot.models import Message
from chat_wars_database.app.guild_helper_bot.models import TelegramUser
from chat_wars_database.app.guild_helper_bot.models import UserDeposits


class TestReportCommand(TestCase):
    def setUp(self) -> None:
        item = Item.objects.create(name="Magic Stone", command="13")
        telegram_user_data = {
            "user_name": "ricardo",
            "name": "@ricardochaves",
            "telegram_id": 1234,
        }
        user = TelegramUser.objects.create(**telegram_user_data)
        self.guild = Guild.objects.create(name="test", captain=user)
        message_data = {
            "chat_id": 65432,
            "forward_date": timezone.now(),
            "message_text": "Deposited successfully: Sanguine Parsley (2)",
            "message_id": 123,
            "telegram_user_id": user.id,
        }
        message = Message.objects.create(**message_data)

        user_deposits_data = {
            "telegram_user": user,
            "message": message,
            "item": item,
            "total": 10,
        }
        UserDeposits.objects.create(**user_deposits_data)

    def test_should_create_a_report(self):
        self.assertIn("What was deposited in the last 7 days.", _execute_report(["/rw"], self.guild))
        self.assertIn("What was deposited in the last 30 days.", _execute_report(["/rm"], self.guild))
        self.assertIn("What was deposited in the last 365 days.", _execute_report(["/ry"], self.guild))

        self.assertIn("What was deposited in the last 7 days.", _execute_report(["/rw", "13"], self.guild))
        self.assertIn("What was deposited in the last 30 days.", _execute_report(["/rm", "13"], self.guild))
        self.assertIn("What was deposited in the last 365 days.", _execute_report(["/ry", "13"], self.guild))
        self.assertIn("The report is for the item 13", _execute_report(["/rw", "13"], self.guild))
        self.assertIn("The report is for the item 13", _execute_report(["/rm", "13"], self.guild))
        self.assertIn("The report is for the item 13", _execute_report(["/ry", "13"], self.guild))

        self.assertIn("What was deposited in the last 7 days.", _execute_report(["/rw", "@ricardochaves"], self.guild))
        self.assertIn("What was deposited in the last 30 days.", _execute_report(["/rm", "@ricardochaves"], self.guild))
        self.assertIn(
            "What was deposited in the last 365 days.", _execute_report(["/ry", "@ricardochaves"], self.guild)
        )
        self.assertIn("Deposits were made by @ricardochaves", _execute_report(["/rw", "@ricardochaves"], self.guild))
        self.assertIn("Deposits were made by @ricardochaves", _execute_report(["/rm", "@ricardochaves"], self.guild))
        self.assertIn("Deposits were made by @ricardochaves", _execute_report(["/ry", "@ricardochaves"], self.guild))

        self.assertIn(
            "What was deposited in the last 7 days.", _execute_report(["/rw", "13", "@ricardochaves"], self.guild)
        )
        self.assertIn(
            "What was deposited in the last 30 days.", _execute_report(["/rm", "13", "@ricardochaves"], self.guild)
        )
        self.assertIn(
            "What was deposited in the last 365 days.", _execute_report(["/ry", "13", "@ricardochaves"], self.guild)
        )
        self.assertIn(
            "Deposits were made by @ricardochaves", _execute_report(["/rw", "@ricardochaves", "13"], self.guild)
        )
        self.assertIn(
            "Deposits were made by @ricardochaves", _execute_report(["/rm", "@ricardochaves", "13"], self.guild)
        )
        self.assertIn(
            "Deposits were made by @ricardochaves", _execute_report(["/ry", "@ricardochaves", "13"], self.guild)
        )
        self.assertIn("The report is for the item 13", _execute_report(["/rw", "@ricardochaves", "13"], self.guild))
        self.assertIn("The report is for the item 13", _execute_report(["/rm", "@ricardochaves", "13"], self.guild))
        self.assertIn("The report is for the item 13", _execute_report(["/ry", "@ricardochaves", "13"], self.guild))
