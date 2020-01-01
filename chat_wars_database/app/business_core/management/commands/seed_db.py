from datetime import timedelta

from django.contrib.auth.models import User
from django.core.management import BaseCommand
from django.utils import timezone

from chat_wars_database.app.business_auction.models import AuctionLot
from chat_wars_database.app.business_core.models import Item
from chat_wars_database.app.business_exchange.models import ExchangeMessages


class Command(BaseCommand):
    def handle(self, *args, **options):

        if not User.objects.filter(username="admin").exists():
            superuser = User.objects.create_superuser(username="admin", password="test")
            superuser.save()

        items = [
            {"command": "r01", "name": "Champion Sword recipe"},
            {"command": "r02", "name": "Trident recipe"},
            {"command": "r03", "name": "Hunter Bow recipe"},
            {"command": "r04", "name": "War hammer recipe"},
            {"command": "r05", "name": "Hunter Dagger recipe"},
            {"command": "r06", "name": "Order Armor recipe"},
            {"command": "r07", "name": "Order Helmet recipe"},
            {"command": "r08", "name": "Order Boots recipe"},
            {"command": "r09", "name": "Order Gauntlets recipe"},
            {"command": "r10", "name": "Order shield recipe"},
            {"command": "r11", "name": "Hunter Armor recipe"},
            {"command": "r12", "name": "Hunter Helmet recipe"},
            {"command": "r13", "name": "Hunter Boots recipe"},
            {"command": "r14", "name": "Hunter Gloves recipe"},
            {"command": "r15", "name": "Clarity Robe recipe"},
            {"command": "r16", "name": "Clarity Circlet recipe"},
            {"command": "r17", "name": "Clarity Shoes recipe"},
            {"command": "r18", "name": "Clarity Bracers recipe"},
            {"command": "r19", "name": "Thundersoul Sword recipe"},
            {"command": "r20", "name": "Doomblade Sword recipe"},
            {"command": "r21", "name": "Eclipse recipe"},
            {"command": "r22", "name": "Guard's Spear recipe"},
            {"command": "r23", "name": "King's Defender recipe"},
            {"command": "r24", "name": "Raging Lance recipe"},
            {"command": "r25", "name": "Composite Bow recipe"},
            {"command": "r26", "name": "Lightning Bow recipe"},
            {"command": "r27", "name": "Hailstorm Bow recipe"},
            {"command": "r28", "name": "Imperial Axe recipe"},
            {"command": "r29", "name": "Skull Crusher recipe"},
            {"command": "r30", "name": "Dragon Mace recipe"},
            {"command": "r31", "name": "Ghost dagger recipe"},
            {"command": "r32", "name": "Lion Knife recipe"},
            {"command": "r33", "name": "Crusader Armor recipe"},
            {"command": "r34", "name": "Crusader Helmet recipe"},
            {"command": "r35", "name": "Crusader Boots recipe"},
            {"command": "r36", "name": "Crusader Gauntlets recipe"},
            {"command": "r37", "name": "Crusader shield recipe"},
            {"command": "r38", "name": "Royal Armor recipe"},
            {"command": "r39", "name": "Royal Helmet recipe"},
            {"command": "r40", "name": "Royal Boots recipe"},
            {"command": "r41", "name": "Royal Gauntlets recipe"},
            {"command": "r42", "name": "Royal shield recipe"},
            {"command": "r43", "name": "Ghost Armor recipe"},
            {"command": "r44", "name": "Ghost Helmet recipe"},
            {"command": "r45", "name": "Ghost Boots recipe"},
            {"command": "r46", "name": "Ghost Gloves recipe"},
            {"command": "r47", "name": "Lion Armor recipe"},
            {"command": "r48", "name": "Lion Helmet recipe"},
            {"command": "r49", "name": "Lion Boots recipe"},
            {"command": "r50", "name": "Lion Gloves recipe"},
            {"command": "r51", "name": "Demon Robe recipe"},
            {"command": "r52", "name": "Demon Circlet recipe"},
            {"command": "r53", "name": "Demon Shoes recipe"},
            {"command": "r54", "name": "Demon Bracers recipe"},
            {"command": "r55", "name": "Divine Robe recipe"},
            {"command": "r56", "name": "Divine Circlet recipe"},
            {"command": "r57", "name": "Divine Shoes recipe"},
            {"command": "r58", "name": "Divine Bracers recipe"},
            {"command": "r59", "name": "Storm Cloak recipe"},
            {"command": "r60", "name": "Durable Cloak recipe"},
            {"command": "r61", "name": "Blessed Cloak recipe"},
            {"command": "r78", "name": "Council Armor recipe"},
            {"command": "r79", "name": "Council Helmet recipe"},
            {"command": "r80", "name": "Council Boots recipe"},
            {"command": "r81", "name": "Council Gauntlets recipe"},
            {"command": "r82", "name": "Council Shield recipe"},
            {"command": "r83", "name": "Griffin Armor recipe"},
            {"command": "r84", "name": "Griffin Helmet recipe"},
            {"command": "r85", "name": "Griffin Boots recipe"},
            {"command": "r86", "name": "Griffin Gloves recipe"},
            {"command": "r87", "name": "Celestial Armor recipe"},
            {"command": "r88", "name": "Celestial Helmet recipe"},
            {"command": "r89", "name": "Celestial Boots recipe"},
            {"command": "r90", "name": "Celestial Bracers recipe"},
            {"command": "r91", "name": "Griffin Knife recipe"},
            {"command": "r92", "name": "Minotaur Sword recipe"},
            {"command": "r93", "name": "Phoenix Sword recipe"},
            {"command": "r94", "name": "Heavy Fauchard recipe"},
            {"command": "r95", "name": "Guisarme recipe"},
            {"command": "r96", "name": "Meteor Bow recipe"},
            {"command": "r97", "name": "Nightfall Bow recipe"},
            {"command": "r98", "name": "Black Morningstar recipe"},
            {"command": "r99", "name": "Maiming Bulawa recipe"},
            {"command": "r100", "name": "Assault Cape recipe"},
            {"command": "r101", "name": "Craftsman Apron recipe"},
            {"command": "r102", "name": "Stoneskin Cloak recipe"},
            {"command": "k01", "name": "Champion blade"},
            {"command": "k02", "name": "Trident blade"},
            {"command": "k03", "name": "Hunter shaft"},
            {"command": "k04", "name": "War hammer head"},
            {"command": "k05", "name": "Hunter blade"},
            {"command": "k06", "name": "Order Armor piece"},
            {"command": "k07", "name": "Order Helmet fragment"},
            {"command": "k08", "name": "Order Boots part"},
            {"command": "k09", "name": "Order Gauntlets part"},
            {"command": "k10", "name": "Order shield part"},
            {"command": "k11", "name": "Hunter Armor part"},
            {"command": "k12", "name": "Hunter Helmet fragment"},
            {"command": "k13", "name": "Hunter Boots part"},
            {"command": "k14", "name": "Hunter Gloves part"},
            {"command": "k15", "name": "Clarity Robe piece"},
            {"command": "k16", "name": "Clarity Circlet fragment"},
            {"command": "k17", "name": "Clarity Shoes part"},
            {"command": "k18", "name": "Clarity Bracers part"},
            {"command": "k19", "name": "Thundersoul blade"},
            {"command": "k20", "name": "Doomblade blade"},
            {"command": "k21", "name": "Eclipse blade"},
            {"command": "k22", "name": "Guard's blade"},
            {"command": "k23", "name": "King's Defender blade"},
            {"command": "k24", "name": "Raging Lance blade"},
            {"command": "k25", "name": "Composite Bow shaft"},
            {"command": "k26", "name": "Lightning Bow shaft"},
            {"command": "k27", "name": "Hailstorm Bow shaft"},
            {"command": "k28", "name": "Imperial Axe head"},
            {"command": "k29", "name": "Skull Crusher head"},
            {"command": "k30", "name": "Dragon Mace head"},
            {"command": "k31", "name": "Ghost blade"},
            {"command": "k32", "name": "Lion blade"},
            {"command": "k33", "name": "Crusader Armor piece"},
            {"command": "k34", "name": "Crusader Helmet fragment"},
            {"command": "k35", "name": "Crusader Boots part"},
            {"command": "k36", "name": "Crusader Gauntlets part"},
            {"command": "k37", "name": "Crusader shield part"},
            {"command": "k38", "name": "Royal Armor piece"},
            {"command": "k39", "name": "Royal Helmet fragment"},
            {"command": "k40", "name": "Royal Boots part"},
            {"command": "k41", "name": "Royal Gauntlets part"},
            {"command": "k42", "name": "Royal shield part"},
            {"command": "k43", "name": "Ghost Armor part"},
            {"command": "k44", "name": "Ghost Helmet fragment"},
            {"command": "k45", "name": "Ghost Boots part"},
            {"command": "k46", "name": "Ghost Gloves part"},
            {"command": "k47", "name": "Lion Armor part"},
            {"command": "k48", "name": "Lion Helmet fragment"},
            {"command": "k49", "name": "Lion Boots part"},
            {"command": "k50", "name": "Lion Gloves part"},
            {"command": "k51", "name": "Demon Robe piece"},
            {"command": "k52", "name": "Demon Circlet fragment"},
            {"command": "k53", "name": "Demon Shoes part"},
            {"command": "k54", "name": "Demon Bracers part"},
            {"command": "k55", "name": "Divine Robe piece"},
            {"command": "k56", "name": "Divine Circlet fragment"},
            {"command": "k57", "name": "Divine Shoes part"},
            {"command": "k58", "name": "Divine Bracers part"},
            {"command": "k59", "name": "Storm Cloak part"},
            {"command": "k60", "name": "Durable Cloak part"},
            {"command": "k61", "name": "Blessed Cloak part"},
            {"command": "k78", "name": "Council Armor part"},
            {"command": "k79", "name": "Council Helmet part"},
            {"command": "k80", "name": "Council Boots part"},
            {"command": "k81", "name": "Council Gauntlets part"},
            {"command": "k82", "name": "Council Shield part"},
            {"command": "k83", "name": "Griffin Armor part"},
            {"command": "k84", "name": "Griffin Helmet part"},
            {"command": "k85", "name": "Griffin Boots part"},
            {"command": "k86", "name": "Griffin Gloves part"},
            {"command": "k87", "name": "Celestial Armor part"},
            {"command": "k88", "name": "Celestial Helmet part"},
            {"command": "k89", "name": "Celestial Boots part"},
            {"command": "k90", "name": "Celestial Bracers part"},
            {"command": "k91", "name": "Griffin Knife part"},
            {"command": "k92", "name": "Minotaur Sword part"},
            {"command": "k93", "name": "Phoenix Sword part"},
            {"command": "k94", "name": "Heavy Fauchard part"},
            {"command": "k95", "name": "Guisarme part"},
            {"command": "k96", "name": "Meteor Bow part"},
            {"command": "k97", "name": "Nightfall Bow part"},
            {"command": "k98", "name": "Black Morningstar part"},
            {"command": "k99", "name": "Maiming Bulawa part"},
            {"command": "k100", "name": "Assault Cape part"},
            {"command": "k101", "name": "Craftsman Apron part"},
            {"command": "k102", "name": "Stoneskin Cloak part"},
            {"command": "a03", "name": "Chain mail"},
            {"command": "a04", "name": "Silver cuirass"},
            {"command": "a05", "name": "Mithril armor"},
            {"command": "a08", "name": "Steel helmet"},
            {"command": "a09", "name": "Silver helmet"},
            {"command": "a10", "name": "Mithril helmet"},
            {"command": "a14", "name": "Silver boots"},
            {"command": "a15", "name": "Mithril boots"},
            {"command": "a19", "name": "Silver gauntlets"},
            {"command": "a20", "name": "Mithril gauntlets"},
            {"command": "a23", "name": "Bronze shield"},
            {"command": "a24", "name": "Silver shield"},
            {"command": "a25", "name": "Mithril shield"},
            {"command": "a26", "name": "Royal Guard Cape"},
            {"command": "a27", "name": "Order Armor"},
            {"command": "a28", "name": "Order Helmet"},
            {"command": "a29", "name": "Order Boots"},
            {"command": "a30", "name": "Order Gauntlets"},
            {"command": "a31", "name": "Order Shield"},
            {"command": "a32", "name": "Hunter Armor"},
            {"command": "a33", "name": "Hunter Helmet"},
            {"command": "a34", "name": "Hunter Boots"},
            {"command": "a35", "name": "Hunter Gloves"},
            {"command": "a36", "name": "Clarity Robe"},
            {"command": "a37", "name": "Clarity Circlet"},
            {"command": "a38", "name": "Clarity Shoes"},
            {"command": "a39", "name": "Clarity Bracers"},
            {"command": "a45", "name": "Crusader Armor"},
            {"command": "a46", "name": "Crusader Helmet"},
            {"command": "a47", "name": "Crusader Boots"},
            {"command": "a48", "name": "Crusader Gauntlets"},
            {"command": "a49", "name": "Crusader Shield"},
            {"command": "a50", "name": "Royal Armor"},
            {"command": "a51", "name": "Royal Helmet"},
            {"command": "a52", "name": "Royal Boots"},
            {"command": "a53", "name": "Royal Gauntlets"},
            {"command": "a54", "name": "Royal Shield"},
            {"command": "a55", "name": "Ghost Armor"},
            {"command": "a56", "name": "Ghost Helmet"},
            {"command": "a57", "name": "Ghost Boots"},
            {"command": "a58", "name": "Ghost Gloves"},
            {"command": "a59", "name": "Lion Armor"},
            {"command": "a60", "name": "Lion Helmet"},
            {"command": "a61", "name": "Lion Boots"},
            {"command": "a62", "name": "Lion Gloves"},
            {"command": "a63", "name": "Demon Robe"},
            {"command": "a64", "name": "Demon Circlet"},
            {"command": "a65", "name": "Demon Shoes"},
            {"command": "a66", "name": "Demon Bracers"},
            {"command": "a67", "name": "Divine Robe"},
            {"command": "a68", "name": "Divine Circlet"},
            {"command": "a69", "name": "Divine Shoes"},
            {"command": "a70", "name": "Divine Bracers"},
            {"command": "a71", "name": "Storm Cloak"},
            {"command": "a72", "name": "Durable Cloak"},
            {"command": "a73", "name": "Blessed Cloak"},
            {"command": "a78", "name": "Council Armor"},
            {"command": "a79", "name": "Council Helmet"},
            {"command": "a80", "name": "Council Boots"},
            {"command": "a81", "name": "Council Gauntlets"},
            {"command": "a82", "name": "Council Shield"},
            {"command": "a83", "name": "Griffin Armor"},
            {"command": "a84", "name": "Griffin Helmet"},
            {"command": "a85", "name": "Griffin Boots"},
            {"command": "a86", "name": "Griffin Gloves"},
            {"command": "a87", "name": "Celestial Armor"},
            {"command": "a88", "name": "Celestial Helmet"},
            {"command": "a89", "name": "Celestial Boots"},
            {"command": "a90", "name": "Celestial Bracers"},
            {"command": "a100", "name": "Assault Cape"},
            {"command": "a101", "name": "Craftsman Apron"},
            {"command": "a102", "name": "Stoneskin Cloak"},
            {"command": "w02", "name": "Short sword"},
            {"command": "w03", "name": "Long sword"},
            {"command": "w04", "name": "Widow sword"},
            {"command": "w05", "name": "Knight's sword"},
            {"command": "w06", "name": "Elven sword"},
            {"command": "w07", "name": "Rapier"},
            {"command": "w09", "name": "Long spear"},
            {"command": "w10", "name": "Lance"},
            {"command": "w11", "name": "Elven spear"},
            {"command": "w12", "name": "Halberd"},
            {"command": "w15", "name": "Steel dagger"},
            {"command": "w16", "name": "Silver dagger"},
            {"command": "w17", "name": "Mithril dagger"},
            {"command": "w19", "name": "Wooden Bow"},
            {"command": "w20", "name": "Long Bow"},
            {"command": "w21", "name": "Elven Bow"},
            {"command": "w22", "name": "Forest Bow"},
            {"command": "w24", "name": "Bone club"},
            {"command": "w25", "name": "Heavy club"},
            {"command": "w26", "name": "Steel axe"},
            {"command": "w27", "name": "Mithril axe"},
            {"command": "w28", "name": "Champion Sword"},
            {"command": "w29", "name": "Trident"},
            {"command": "w30", "name": "Hunter Bow"},
            {"command": "w31", "name": "War hammer"},
            {"command": "w32", "name": "Hunter dagger"},
            {"command": "w33", "name": "Thundersoul Sword"},
            {"command": "w34", "name": "Doomblade Sword"},
            {"command": "w35", "name": "Eclipse"},
            {"command": "w36", "name": "Guard's Spear"},
            {"command": "w37", "name": "King's Defender"},
            {"command": "w38", "name": "Raging Lance"},
            {"command": "w39", "name": "Composite Bow"},
            {"command": "w40", "name": "Lightning Bow"},
            {"command": "w41", "name": "Hailstorm Bow"},
            {"command": "w42", "name": "Imperial Axe"},
            {"command": "w43", "name": "Skull Crusher"},
            {"command": "w44", "name": "Dragon Mace"},
            {"command": "w45", "name": "Ghost dagger"},
            {"command": "w46", "name": "Lion Knife"},
            {"command": "w91", "name": "Griffin Knife"},
            {"command": "w92", "name": "Minotaur Sword"},
            {"command": "w93", "name": "Phoenix Sword"},
            {"command": "w94", "name": "Heavy Fauchard"},
            {"command": "w95", "name": "Guisarme"},
            {"command": "w96", "name": "Meteor Bow"},
            {"command": "w97", "name": "Nightfall Bow"},
            {"command": "w98", "name": "Black Morningstar"},
            {"command": "w99", "name": "Maiming Bulawa"},
            {"command": "s01", "name": "📕Scroll of Rage"},
            {"command": "s02", "name": "📕Scroll of Peace"},
            {"command": "s03", "name": "📗Scroll of Rage"},
            {"command": "s04", "name": "📗Scroll of Peace"},
            {"command": "s05", "name": "📘Scroll of Rage"},
            {"command": "s06", "name": "📘Scroll of Peace"},
            {"command": "s11", "name": "📕Rare scroll of Rage"},
            {"command": "s12", "name": "📕Rare scroll of Peace"},
            {"command": "s13", "name": "📗Rare scroll of Rage"},
            {"command": "s14", "name": "📗Rare scroll of Peace"},
            {"command": "s15", "name": "📘Rare scroll of Rage"},
            {"command": "s16", "name": "📘Rare scroll of Peace"},
            {"command": "s50", "name": "🖋Scroll of Engraving"},
            {"command": "s51", "name": "✒️Scroll of Engraving"},
            {"command": "s07", "name": "📙Scroll of Rage"},
            {"command": "s08", "name": "📙Scroll of Peace"},
            {"command": "s17", "name": "📙Rare scroll of Rage"},
            {"command": "s18", "name": "📙Rare scroll of Peace"},
            {"command": "e101", "name": "🧟‍♂️ Witchling Robe"},
            {"command": "e102", "name": "🧟‍♂️ Witchling Circlet"},
            {"command": "e103", "name": "🧟‍♂️ Witchling Shoes"},
            {"command": "e104", "name": "🧟‍♂️ Witchling Bracers"},
            {"command": "e105", "name": "🧟‍♂️ Witch Robe"},
            {"command": "e106", "name": "🧟‍♂️ Witch Circlet"},
            {"command": "e107", "name": "🧟‍♂️ Witch Shoes"},
            {"command": "e108", "name": "🧟‍♂️ Witch Bracers"},
            {"command": "e109", "name": "🧟‍♂️ Walker Armor"},
            {"command": "e110", "name": "🧟‍♂️ Walker Helmet"},
            {"command": "e111", "name": "🧟‍♂️ Walker Boots"},
            {"command": "e112", "name": "🧟‍♂️ Walker Gauntlets"},
            {"command": "e113", "name": "🧟‍♂️ Walker Shield"},
            {"command": "e114", "name": "🧟‍♂️ Zombie Armor"},
            {"command": "e115", "name": "🧟‍♂️ Zombie Helmet"},
            {"command": "e116", "name": "🧟‍♂️ Zombie Boots"},
            {"command": "e117", "name": "🧟‍♂️ Zombie Gauntlets"},
            {"command": "e118", "name": "🧟‍♂️ Zombie Shield"},
            {"command": "e119", "name": "🧟‍♂️ Imp Robe"},
            {"command": "e120", "name": "🧟‍♂️ Imp Circlet"},
            {"command": "e121", "name": "🧟‍♂️ Imp Shoes"},
            {"command": "e122", "name": "🧟‍♂️ Imp Bracers"},
            {"command": "e123", "name": "🧟‍♂️ Demon Robe"},
            {"command": "e124", "name": "🧟‍♂️ Demon Circlet"},
            {"command": "e125", "name": "🧟‍♂️ Demon Shoes"},
            {"command": "e126", "name": "🧟‍♂️ Demon Bracers"},
            {"command": "e127", "name": "🧟‍♂️ Manwolf Armor"},
            {"command": "e128", "name": "🧟‍♂️ Manwolf Helmet"},
            {"command": "e129", "name": "🧟‍♂️ Manwolf Boots"},
            {"command": "e130", "name": "🧟‍♂️ Manwolf Gloves"},
            {"command": "e131", "name": "🧟‍♂️ Werewolf Armor"},
            {"command": "e132", "name": "🧟‍♂️ Werewolf Helmet"},
            {"command": "e133", "name": "🧟‍♂️ Werewolf Boots"},
            {"command": "e134", "name": "🧟‍♂️ Werewolf Gloves"},
            {"command": "e135", "name": "🧟‍♂️ Fleder Armor"},
            {"command": "e136", "name": "🧟‍♂️ Fleder Helmet"},
            {"command": "e137", "name": "🧟‍♂️ Fleder Boots"},
            {"command": "e138", "name": "🧟‍♂️ Fleder Gloves"},
            {"command": "e139", "name": "🧟‍♂️ Nosferatu Armor"},
            {"command": "e140", "name": "🧟‍♂️ Nosferatu Helmet"},
            {"command": "e141", "name": "🧟‍♂️ Nosferatu Boots"},
            {"command": "e142", "name": "🧟‍♂️ Nosferatu Gloves"},
            {"command": "e143", "name": "🧟‍♂️ Witchling Staff"},
            {"command": "e144", "name": "🧟‍♂️ War Club"},
            {"command": "e145", "name": "🧟‍♂️ Imp Bow"},
            {"command": "e146", "name": "🧟‍♂️ Imp Whip"},
            {"command": "e147", "name": "🧟‍♂️ Manwolf Knife"},
            {"command": "e148", "name": "🧟‍♂️ Fleder Scimitar"},
            {"command": "e149", "name": "🧟‍♂️ Witch Staff"},
            {"command": "e150", "name": "🧟‍♂️ Walker Club"},
            {"command": "e151", "name": "🧟‍♂️ Demon Bow"},
            {"command": "e152", "name": "🧟‍♂️ Demon Whip"},
            {"command": "e153", "name": "🧟‍♂️ Werewolf Knife"},
            {"command": "e154", "name": "🧟‍♂️ Nosferatu Rapier"},
            {"command": "e156", "name": "Hat of Pretender"},
            {"command": "614", "name": "🎟Gift Coupon 'Pig'"},
            {"command": "615", "name": "🎟Gift Coupon 'Horse'"},
            {"command": "616", "name": "🎟Gift Coupon 'Owl'"},
            {"command": "617", "name": "🎟Gift Coupon 'Mouse'"},
            {"command": "622", "name": "🎟Gift Coupon 'Gopher'"},
            {"command": "623", "name": "🎟Gift Coupon 'Ants'"},
            {"command": "624", "name": "🎟Gift Coupon 'Spider'"},
            {"command": "625", "name": "🎟Gift Coupon 'Haunted'"},
            {"command": "626", "name": "🎟Gift Coupon 'Camel'"},
        ]

        ents = []
        for i in items:
            ents.append(Item(command=i["command"], name=i["name"]))

        Item.objects.bulk_create(ents)

        Item.objects.create(
            name="Potion of Rage",
            command="r122",
            tradeable_exchange=True,
            tradeable_auction=False,
            craftable=True,
            depositable_in_guild=False,
            event_item=True,
            can_be_found_in_quests=False,
            craft_command="/craft_r12",
            mana_crafting=12,
            skill_craft_level=1,
            weight=2,
            base_duration=20,
            quest_forest_day=False,
            quest_swamp_day=False,
            quest_valley_day=False,
            quest_foray_day=False,
            quest_forest_morning=False,
            quest_swamp_morning=True,
            quest_valley_morning=False,
            quest_foray_morning=False,
            quest_forest_evening=False,
            quest_swamp_evening=False,
            quest_valley_evening=False,
            quest_foray_evening=False,
            quest_forest_night=False,
            quest_swamp_night=False,
            quest_valley_night=False,
            quest_foray_night=False,
        )

        AuctionLot.objects.create(
            item=Item.objects.filter(command="s07").first(),
            auction_item="Weapon",
            message_id="1",
            lot_id=123456,
            seller_name="XXX",
            seller_castle="X",
            started_price=1,
            message_date=timezone.now(),
            quality=1,
            price=1,
            status=1,
            real_time_end_at=timezone.now(),
            end_at="14 Ōstar 1065 05:32",
        )

        AuctionLot.objects.create(
            item=Item.objects.filter(command="s07").first(),
            auction_item="Weapon",
            message_id="2",
            lot_id=123457,
            seller_name="YYY",
            seller_castle="Y",
            started_price=1,
            message_date=timezone.now() + timedelta(days=1),
            quality=1,
            price=10,
            status=1,
            real_time_end_at=timezone.now() + timedelta(days=3),
            end_at="14 Ōstar 1065 05:32",
        )
        AuctionLot.objects.create(
            item=Item.objects.filter(command="s07").first(),
            auction_item="Weapon",
            message_id="3",
            lot_id=123458,
            seller_name="YYY",
            seller_castle="Y",
            started_price=1,
            message_date=timezone.now() + timedelta(days=2),
            quality=1,
            price=10,
            status=1,
            real_time_end_at=timezone.now() + timedelta(days=4),
            end_at="14 Ōstar 1065 05:32",
        )

        AuctionLot.objects.create(
            item=Item.objects.filter(command="r122").first(),
            auction_item="Weapon",
            message_id="7",
            lot_id=123459,
            seller_name="YYY",
            seller_castle="Y",
            started_price=1,
            message_date=timezone.now() + timedelta(days=2),
            quality=1,
            price=10,
            status=1,
            real_time_end_at=timezone.now() + timedelta(days=4),
            end_at="14 Ōstar 1065 05:32",
        )

        ExchangeMessages.objects.create(
            message_id=1234,
            message_date=timezone.now(),
            message_text="""Silver ore:
🌑Daniel => 🦌4KHunter, 5 x 1💰
🌑Daniel => 🐉Connor Kenway, 6 x 1💰
Thread:
🌑Minion => 🦌Thorin, 5 x 7💰
🌑Minion => 🦅TiTo7170, 5 x 7💰
🌑Minion => 🦌Thorin, 4 x 7💰
Rope:
🐺InsertNameHere => 🦌Pirate_Warrior, 9 x 5💰
Pelt:
🐺Sayur Kol => 🐺Bloodhunter, 1 x 1💰""",
        )

        ExchangeMessages.objects.create(
            message_id=1235,
            message_date=timezone.now(),
            message_text="""Pelt:
🦌Medivh => 🐺Bloodhunter, 1 x 1💰
🐺Zafit => 🐺Bloodhunter, 1 x 1💰
Coal:
🌑Taneleer Tivan => 🥔Malte, 1 x 1💰
🐺GrumpyGecko => 🥔Malte, 1 x 1💰
Cloth:
🦈Angela => 🐺Silverstream, 1 x 1💰
Sapphire:
🌑Taneleer Tivan => 🥔Malte, 1 x 1💰
🦅devi => 🥔Malte, 1 x 1💰
Magic stone:
🥔Moka => 🥔Malte, 1 x 31💰
Thread:
🌑Minion => 🦅LuluVi0, 5 x 7💰
Bauxite:
🐺Panfilo => 🥔Malte, 1 x 1💰
🦅devi => 🥔Malte, 1 x 1💰
🦌Ilvatar => 🥔Malte, 1 x 1💰""",
        )
