from django.test import TestCase
from django.utils import timezone

from chat_wars_database.app.guild_helper_bot.commands import _execute_deposit
from chat_wars_database.app.guild_helper_bot.models import Message
from chat_wars_database.app.guild_helper_bot.models import UserDeposits


class TestDepositEvent(TestCase):
    def test_should_create_message(self):
        telegram_user_data = {
            "user_name": "ricardo",
            "name": "Ricardo",
            "telegram_id": 123456433,
        }

        message_data = {
            "chat_id": 8765432,
            "forward_date": timezone.now(),
            "message_text": "Deposited successfully: Magic stone (1)",
            "message_id": 12345676543,
        }

        _execute_deposit(telegram_user_data, message_data)
        _execute_deposit(telegram_user_data, message_data)

        self.assertEqual(Message.objects.count(), 1)
        self.assertEqual(UserDeposits.objects.count(), 1)

        message_data["forward_date"] = timezone.now()

        _execute_deposit(telegram_user_data, message_data)

        self.assertEqual(Message.objects.count(), 2)
        self.assertEqual(UserDeposits.objects.count(), 2)

        message_data = {
            "chat_id": 8765432,
            "forward_date": timezone.now(),
            "message_text": "Deposited successfully: Silver ore (281)",
            "message_id": 12345676543,
        }

        _execute_deposit(telegram_user_data, message_data)

        self.assertEqual(Message.objects.count(), 3)
        self.assertEqual(UserDeposits.objects.count(), 3)

        u = UserDeposits.objects.filter(item__name__exact="Silver ore").first()

        self.assertEqual(u.total, 281)
