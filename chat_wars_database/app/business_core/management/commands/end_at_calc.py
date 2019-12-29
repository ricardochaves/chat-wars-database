import logging

from django.core.management import BaseCommand

from chat_wars_database.app.business_auction.business import convert_game_date_to_real_date
from chat_wars_database.app.business_auction.models import AuctionLot

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):

        lot = AuctionLot.objects.order_by("id").first()

        while lot:
            logger.info("Lot id: %s", lot.id)
            dt = convert_game_date_to_real_date(lot.end_at)
            lot.real_time_end_at = dt
            lot.save()

            lot = AuctionLot.objects.filter(id__gt=lot.id).order_by("id").first()
