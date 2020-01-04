from collections import Counter
from typing import Dict
from typing import Optional

from chat_wars_database.app.business_auction.models import AuctionLot
from chat_wars_database.app.business_core.models import Item


def _build_top_castle_seller(  # pylint: disable = too-many-arguments
    deerhorn: int, dragonscale: int, highnest: int, moonlight: int, potato: int, sharkteeth: int, wolfpack: int
) -> str:
    message = ""
    d = {"🦌": deerhorn, "🐉": dragonscale, "🦅": highnest, "🌑": moonlight, "🥔": potato, "🦈": sharkteeth, "🐺": wolfpack}

    c = Counter(d)

    ordered_list = c.most_common()

    for i in ordered_list:
        message += f"\n{i[0]} - {i[1]}"

    return message


def build_item_message_exchange(exchange_data: Dict, item: Item) -> str:

    top_seller_castle_message = _build_top_castle_seller(
        exchange_data["deerhorn_castle_seller"],
        exchange_data["dragonscale_castle_seller"],
        exchange_data["highnest_castle_seller"],
        exchange_data["moonlight_castle_seller"],
        exchange_data["potato_castle_seller"],
        exchange_data["sharkteeth_castle_seller"],
        exchange_data["wolfpack_castle_seller"],
    )

    top_buyer_castle_message = _build_top_castle_seller(
        exchange_data["deerhorn_castle_buyer"],
        exchange_data["dragonscale_castle_buyer"],
        exchange_data["highnest_castle_buyer"],
        exchange_data["moonlight_castle_buyer"],
        exchange_data["potato_castle_buyer"],
        exchange_data["sharkteeth_castle_buyer"],
        exchange_data["wolfpack_castle_buyer"],
    )

    return f"""{item.name} for ~ {exchange_data['avg_price_30_days']} 💰

All data is from the last 30 days.

Most Expensive {exchange_data['max_value']}💰 on {exchange_data['max_value_date']} - [Link](t.me/chtwrsExchange/{exchange_data['max_value_message_id']})
Cheapest {exchange_data['min_value']}💰 on {exchange_data['min_value_date']} - [Link](t.me/chtwrsExchange/{exchange_data['min_value_message_id']})

Total units sold: {exchange_data['total_sold']}

Total units purchased per castle:{top_buyer_castle_message}

Total units sold per castle:{top_seller_castle_message}

{build_general_data(item)}
{build_graph_message(item)}"""


def build_item_message_auction(lots_data: Dict, item: Item) -> str:

    curiosities = build_lots_curiosities(lots_data)

    return f"""{item.name} for ~ {lots_data['total_week_median']} 👝

Total: {lots_data['total_life']}
Times sold: {lots_data['total_life_sold']}
Last sold: {lots_data['last_sold']}

All time:
Median: {lots_data['total_life_median']}
Average: {lots_data['total_life_average']}
Min/Max: {lots_data['total_life_min']}/{lots_data['total_life_max']}
Unsold: {lots_data['total_life_unsold']}/{lots_data['total_life']}

Last 7 days:
Median: {lots_data['total_week_median']}
Average: {lots_data['total_week_average']}
Min/Max: {lots_data['total_week_min']}/{lots_data['total_week_max']}
Unsold: {lots_data['total_week_unsold']}/{lots_data['total_week']}
{curiosities}
{build_general_data(item)}
{build_graph_message(item)}"""


def build_lots_curiosities(data: Dict) -> str:
    first_lot: Optional[AuctionLot] = data["first_lot"]
    last_lot: Optional[AuctionLot] = data["last_lot"]
    cheaper_lot: Optional[AuctionLot] = data["cheaper_lot"]
    more_expensive: Optional[AuctionLot] = data["more_expensive"]

    message = ""

    if first_lot:
        message += f"\nFirst: [Lot {first_lot.lot_id}](t.me/ChatWarsAuction/{first_lot.message_id})"

    if last_lot:
        message += f"\nLast: [Lot {last_lot.lot_id}](t.me/ChatWarsAuction/{last_lot.message_id})"

    if cheaper_lot:
        message += f"\nCheapest: [Lot {cheaper_lot.lot_id}](t.me/ChatWarsAuction/{cheaper_lot.message_id}) - {cheaper_lot.price} 👝"  # pylint: disable = line-too-long # noqa

    if more_expensive:
        message += f"\nMost Expensive: [Lot {more_expensive.lot_id}](t.me/ChatWarsAuction/{more_expensive.message_id}) - {more_expensive.price} 👝"  # pylint: disable = line-too-long # noqa

    if message:
        message = f"\nCuriosities:\n{message}\n"

    return message


def build_tradeable_exchange(i: Item) -> str:

    if i.tradeable_exchange:
        return f"✅ (command /t\_{i.command})"

    return "❌"


def print_string(data: Optional[str]) -> str:

    return data if data else ""


def print_boolean(data: Optional[bool]) -> str:

    return "✅" if data else "❌"


def build_general_data(item: Item) -> str:
    return f"""Depositable in Guild: {print_boolean(item.depositable_in_guild)}
Event item: {print_boolean(item.event_item)}
Craftable: {print_boolean(item.craftable)}
Tradeable (Exchange): {build_tradeable_exchange(item)}
Tradeable (Auction): {print_boolean(item.tradeable_auction)}
    """


def build_graph_message(item: Item) -> str:
    return f"""See the graphics: 
Last 30 days: /g\_{item.command}\_30
All the history: /g\_{item.command}"""
