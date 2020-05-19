from django.core.management import BaseCommand

from chat_wars_database.app.craft.business import update_all_crafted_items


class Command(BaseCommand):
    def handle(self, *args, **options):
        update_all_crafted_items()
