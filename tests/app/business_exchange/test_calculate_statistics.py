import datetime
from decimal import Decimal

from django.test import TestCase
from django.utils.timezone import make_aware

from chat_wars_database.app.business_exchange.management.commands.calculate_statistics import apply_regex_for_each_line
from chat_wars_database.app.business_exchange.management.commands.calculate_statistics import calculate
from chat_wars_database.app.business_exchange.models import ExchangeMessages
from chat_wars_database.app.business_exchange.models import StatsByDay


class TestCalculateExchangeCommands(TestCase):
    def test_regex_should_extract_correct_information(self):

        self.assertEqual(apply_regex_for_each_line("🥔SmashinDeezNuts => 🥔Malte, 1 x 1💰").group("quantity"), "1")
        self.assertEqual(apply_regex_for_each_line("🦌whitetale => 🌑Taneleer Tivan, 15 x 5💰").group("quantity"), "15")
        self.assertEqual(apply_regex_for_each_line("🌑Minion => 🦅LuluVi0, 1 x 7💰").group("quantity"), "1")
        self.assertEqual(apply_regex_for_each_line("🌑Minion => 🦈Minie, 3 x 7💰").group("quantity"), "3")
        self.assertEqual(apply_regex_for_each_line("🌑Minion => 🐉Rasputin, 10 x 7💰").group("quantity"), "10")
        self.assertEqual(apply_regex_for_each_line("🥔Malte => 🐉Sun Wokong, 15 x 6💰").group("quantity"), "15")
        self.assertEqual(apply_regex_for_each_line("🐺Silverstream => 🐉Sun Wokong, 30 x 6💰").group("quantity"), "30")
        self.assertEqual(apply_regex_for_each_line("🐺MegaDeth => 🥔Malte, 1 x 100💰").group("quantity"), "1")
        self.assertEqual(apply_regex_for_each_line("🦌Ilvatar => 🥔Malte, 573 x 1💰").group("quantity"), "573")
        self.assertEqual(apply_regex_for_each_line("🥔MORGANA => 🐺PABLO ESCOBAR, 1 x 2💰").group("quantity"), "1")
        self.assertEqual(apply_regex_for_each_line("🐉iBittz => 🐺Silverstream, 13 x 6💰").group("quantity"), "13")
        self.assertEqual(apply_regex_for_each_line("🥔Moka => 🥔Malte, 1 x 31💰").group("quantity"), "1")

        self.assertEqual(apply_regex_for_each_line("🥔SmashinDeezNuts => 🥔Malte, 1 x 1💰").group("value"), "1")
        self.assertEqual(apply_regex_for_each_line("🦌whitetale => 🌑Taneleer Tivan, 15 x 5💰").group("value"), "5")
        self.assertEqual(apply_regex_for_each_line("🌑Minion => 🦅LuluVi0, 1 x 7💰").group("value"), "7")
        self.assertEqual(apply_regex_for_each_line("🌑Minion => 🦈Minie, 3 x 7💰").group("value"), "7")
        self.assertEqual(apply_regex_for_each_line("🌑Minion => 🐉Rasputin, 10 x 7💰").group("value"), "7")
        self.assertEqual(apply_regex_for_each_line("🥔Malte => 🐉Sun Wokong, 15 x 6💰").group("value"), "6")
        self.assertEqual(apply_regex_for_each_line("🐺Silverstream => 🐉Sun Wokong, 30 x 6💰").group("value"), "6")
        self.assertEqual(apply_regex_for_each_line("🐺MegaDeth => 🥔Malte, 1 x 1💰").group("value"), "1")
        self.assertEqual(apply_regex_for_each_line("🦌Ilvatar => 🥔Malte, 1 x 100💰").group("value"), "100")
        self.assertEqual(apply_regex_for_each_line("🥔MORGANA => 🐺PABLO ESCOBAR, 1 x 2💰").group("value"), "2")
        self.assertEqual(apply_regex_for_each_line("🐉iBittz => 🐺Silverstream, 13 x 6💰").group("value"), "6")
        self.assertEqual(apply_regex_for_each_line("🥔Moka => 🥔Malte, 1 x 31💰").group("value"), "31")

        self.assertEqual(apply_regex_for_each_line("🥔SmashinDeezNuts => 🥔Malte, 1 x 1💰").group()[3], "🥔")
        self.assertEqual(apply_regex_for_each_line("🦌whitetale => 🌑Taneleer Tivan, 15 x 5💰").group()[3], "🌑")
        self.assertEqual(apply_regex_for_each_line("🌑Minion => 🦅LuluVi0, 1 x 7💰").group()[3], "🦅")
        self.assertEqual(apply_regex_for_each_line("🌑Minion => 🦈Minie, 3 x 7💰").group()[3], "🦈")
        self.assertEqual(apply_regex_for_each_line("🌑Minion => 🐉Rasputin, 10 x 7💰").group()[3], "🐉")
        self.assertEqual(apply_regex_for_each_line("🥔Malte => 🐉Sun Wokong, 15 x 6💰").group()[3], "🐉")
        self.assertEqual(apply_regex_for_each_line("🐺Silverstream => 🐉Sun Wokong, 30 x 6💰").group()[3], "🐉")
        self.assertEqual(apply_regex_for_each_line("🐺MegaDeth => 🥔Malte, 1 x 1💰").group()[3], "🥔")
        self.assertEqual(apply_regex_for_each_line("🦌Ilvatar => 🥔Malte, 1 x 1💰").group()[3], "🥔")
        self.assertEqual(apply_regex_for_each_line("🥔MORGANA => 🐺PABLO ESCOBAR, 1 x 2💰").group()[3], "🐺")
        self.assertEqual(apply_regex_for_each_line("🐉iBittz => 🐺Silverstream, 13 x 6💰").group()[3], "🐺")
        self.assertEqual(apply_regex_for_each_line("🥔Moka => 🥔Malte, 1 x 31💰").group()[3], "🥔")

    def test_should_create_daily_stats(self):
        dt = make_aware(datetime.datetime(1981, 6, 21)).date()
        ExchangeMessages.objects.create(
            message_id=1,
            message_date=dt,
            message_text="""Pelt:
🦌Medivh => 🐺Bloodhunter, 1 x 2💰
🐺Zafit => 🐺Bloodhunter, 2 x 1💰
Coal:
🌑Taneleer Tivan => 🥔Malte, 2 x 10💰
🐺GrumpyGecko => 🥔Malte, 2 x 1💰""",
        )

        calculate(dt)

        self.assertEqual(StatsByDay.objects.count(), 2)

        st: StatsByDay = StatsByDay.objects.filter(item__name="Pelt").first()

        self.assertEqual(st.date, dt)
        self.assertEqual(st.min_value, 1)
        self.assertEqual(st.max_value, 2)
        self.assertEqual(st.units, 3)

        self.assertEqual(st.deerhorn_castle_seller, 1)
        self.assertEqual(st.deerhorn_castle_buyer, 0)
        self.assertEqual(st.dragonscale_castle_seller, 0)
        self.assertEqual(st.dragonscale_castle_buyer, 0)
        self.assertEqual(st.highnest_castle_seller, 0)
        self.assertEqual(st.highnest_castle_buyer, 0)
        self.assertEqual(st.moonlight_castle_seller, 0)
        self.assertEqual(st.moonlight_castle_buyer, 0)
        self.assertEqual(st.potato_castle_seller, 0)
        self.assertEqual(st.potato_castle_buyer, 0)
        self.assertEqual(st.sharkteeth_castle_seller, 0)
        self.assertEqual(st.sharkteeth_castle_buyer, 0)
        self.assertEqual(st.wolfpack_castle_seller, 2)
        self.assertEqual(st.wolfpack_castle_buyer, 3)

        self.assertAlmostEquals(st.average_value, Decimal(1.33))
        self.assertEqual(st.mean_value, 1)

        st: StatsByDay = StatsByDay.objects.filter(item__name="Coal").first()

        self.assertEqual(st.date, dt)
        self.assertEqual(st.min_value, 1)
        self.assertEqual(st.max_value, 10)
        self.assertEqual(st.units, 4)

        self.assertEqual(st.deerhorn_castle_seller, 0)
        self.assertEqual(st.deerhorn_castle_buyer, 0)
        self.assertEqual(st.dragonscale_castle_seller, 0)
        self.assertEqual(st.dragonscale_castle_buyer, 0)
        self.assertEqual(st.highnest_castle_seller, 0)
        self.assertEqual(st.highnest_castle_buyer, 0)
        self.assertEqual(st.moonlight_castle_seller, 2)
        self.assertEqual(st.moonlight_castle_buyer, 0)
        self.assertEqual(st.potato_castle_seller, 0)
        self.assertEqual(st.potato_castle_buyer, 4)
        self.assertEqual(st.sharkteeth_castle_seller, 0)
        self.assertEqual(st.sharkteeth_castle_buyer, 0)
        self.assertEqual(st.wolfpack_castle_seller, 2)
        self.assertEqual(st.wolfpack_castle_buyer, 0)

        self.assertAlmostEquals(st.average_value, Decimal(5.5))
        self.assertEqual(st.mean_value, 5)
