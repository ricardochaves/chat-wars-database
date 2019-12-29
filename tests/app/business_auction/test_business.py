import datetime

import pytz
from django.test import TestCase

from chat_wars_database.app.business_auction.business import convert_game_date_to_real_date


class TestExecuteMessageTest(TestCase):
    def test_should_convert_date(self):

        self.assertEqual(
            convert_game_date_to_real_date("14 Ōstar 1065 12:55"),
            datetime.datetime(2019, 12, 23, 17, 19, 8, tzinfo=pytz.UTC),
        )

        self.assertEqual(
            convert_game_date_to_real_date("12 Ōstar 1065 19:34"),
            datetime.datetime(2019, 12, 23, 3, 32, 8, tzinfo=pytz.UTC),
        )

        self.assertEqual(
            convert_game_date_to_real_date("13 Ōstar 1065 22:10"),
            datetime.datetime(2019, 12, 23, 12, 24, 8, tzinfo=pytz.UTC),
        )

        self.assertEqual(
            convert_game_date_to_real_date("13 Ōstar 1065 00:46"),
            datetime.datetime(2019, 12, 23, 5, 16, 8, tzinfo=pytz.UTC),
        )
        self.assertEqual(
            convert_game_date_to_real_date("17 Ōstar 1065 21:48"),
            datetime.datetime(2019, 12, 24, 20, 16, 48, tzinfo=pytz.UTC),
        )
