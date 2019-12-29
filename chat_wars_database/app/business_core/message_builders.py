from typing import Dict
from typing import Optional

from chat_wars_database.app.business_auction.models import AuctionLot
from chat_wars_database.app.business_core.models import Item


def build_item_message(data: Dict, item: Item) -> str:

    curiosities = build_lots_curiosities(data)

    return f"""
{item.name} for ~ {data['total_week_median']} 👝

Total: {data['total_life']}
Times sold: {data['total_life_sold']}
Last sold: {data['last_sold']}

All time:
Median: {data['total_life_median']}
Average: {data['total_life_average']}
Min/Max: {data['total_life_min']}/{data['total_life_max']}
Unsold: {data['total_life_unsold']}/{data['total_life']}

Last 7 days:
Median: {data['total_week_median']}
Average: {data['total_week_average']}
Min/Max: {data['total_week_min']}/{data['total_week_max']}
Unsold: {data['total_week_unsold']}/{data['total_week']}

Curiosities:
{curiosities}
    """


def build_lots_curiosities(data: Dict) -> str:
    first_lot: Optional[AuctionLot] = data["first_lot"]
    last_lot: Optional[AuctionLot] = data["last_lot"]
    cheaper_lot: Optional[AuctionLot] = data["cheaper_lot"]
    more_expensive: Optional[AuctionLot] = data["more_expensive"]

    message = ""

    if first_lot:
        message += f"\nFirst: [Lot {first_lot.lot_id}](https://t.me/ChatWarsAuction/{first_lot.message_id})"

    if last_lot:
        message += f"\nLast: [Lot {last_lot.lot_id}](https://t.me/ChatWarsAuction/{last_lot.message_id})"

    if cheaper_lot:
        message += f"\nCheaper: [Lot {cheaper_lot.lot_id}](https://t.me/ChatWarsAuction/{cheaper_lot.message_id}) - {cheaper_lot.price} 👝"  # pylint: disable = line-too-long # noqa

    if more_expensive:
        message += f"\nMore Expensive: [Lot {more_expensive.lot_id}](https://t.me/ChatWarsAuction/{more_expensive.message_id}) - {more_expensive.price} 👝"  # pylint: disable = line-too-long # noqa

    return message
