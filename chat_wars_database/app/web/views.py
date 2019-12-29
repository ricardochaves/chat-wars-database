from datetime import timedelta

from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.utils import timezone

from chat_wars_database.app.web.db_results import get_all_items
from chat_wars_database.app.web.db_results import get_auctions_average
from chat_wars_database.app.web.db_results import get_cheaper_lot
from chat_wars_database.app.web.db_results import get_first_lot
from chat_wars_database.app.web.db_results import get_first_lot_in_db
from chat_wars_database.app.web.db_results import get_item_from_command
from chat_wars_database.app.web.db_results import get_last_lot
from chat_wars_database.app.web.db_results import get_more_expensive
from chat_wars_database.app.web.db_results import get_more_expensive_lot
from chat_wars_database.app.web.db_results import get_total_active_lots


def index(request):

    return render(
        request,
        "web/index.html",
        context={
            "lot": get_more_expensive_lot(),
            "first_lot": get_first_lot_in_db(),
            "total_active_lots": get_total_active_lots(),
            "items": get_all_items(),
        },
    )


def auction_item(request, command: str):

    item = get_item_from_command(command)

    if not item:
        return HttpResponseNotFound("<h1>Page not found</h1>")

    host = f"{request.scheme}://{request.get_host()}"

    items = get_auctions_average(command)

    data = []
    data_last_month = []

    for i in items:
        data.append([i["d"].year, i["d"].month, i["d"].day, i["price__avg"]])

        if i["d"] > (timezone.now() - timedelta(days=30)).date():
            data_last_month.append([i["d"].year, i["d"].month, i["d"].day, i["price__avg"]])

    return render(
        request,
        "web/auction_item.html",
        context={
            "data": data,
            "host": host,
            "item": item,
            "data_last_month": data_last_month,
            "first_lot": get_first_lot(command),
            "last_lot": get_last_lot(command),
            "cheaper_lot": get_cheaper_lot(command),
            "more_expensive": get_more_expensive(command),
        },
    )
