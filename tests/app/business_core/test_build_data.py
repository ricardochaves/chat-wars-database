from django.test import TestCase

from chat_wars_database.app.business_auction.business import _build_data


class TestBuildData(TestCase):
    def test_build_data_with_quality_message(self):

        expected_data = {
            "lot_id": 381570,
            "seller_name": "[NVR]Cernunnos",
            "seller_castle": "🦌",
            "price": 71,
            "buyer_name": None,
            "buyer_castle": "🐺",
            "status": 1,
            "end_at": "10 Lenzin 1065 10:49",
            "item": "Crusader Armor",
            "auction_item": "Crusader Armor +15⚔️ +37🛡",
            "quality": 5,
        }

        data = _build_data(
            """Lot #381570 : Crusader Armor +15⚔️ +37🛡
Quality: Masterpiece
Seller: 🦌 [NVR]Cernunnos
Current price: 71 pouch(es)
Buyer: 🐺
End At: 10 Lenzin 1065 10:49
Status: #active

/bet_381570"""
        )

        self.assertDictEqual(expected_data, data)
