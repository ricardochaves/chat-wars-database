import logging
from time import sleep

from django.db import transaction

from chat_wars_database.app.business_core.management.commands.update_items import get_item_data
from chat_wars_database.app.business_core.models import Item
from chat_wars_database.app.business_core.models import Recipe

logger = logging.getLogger(__name__)

SPACES_FOR_CRAFT_MESSAGE = "  "


def update_recipe_item(item: Item) -> None:

    recipes = []
    item_data = get_item_data(item)
    for subject in item_data["sobj"]:
        it = None
        qtd = None
        for d in subject["data"]:
            if d["property"] == "Crafting_ingredient":
                item_name = d["dataitem"][0]["item"].split("#")[0].replace("_", " ").lower()
                it = Item.objects.filter(name__iexact=item_name).first()
                if not it:
                    raise Exception(f"Item not found. Name: {item_name}")
            if d["property"] == "Qty":
                qtd = int(d["dataitem"][0]["item"])

        if it and qtd:
            recipes.append(Recipe(ingredient=it, amount=qtd, item=item))

    with transaction.atomic():
        Recipe.objects.filter(item=item).delete()
        Recipe.objects.bulk_create(recipes)


def update_all_crafted_items():
    logger.info("Starting...")

    items = Item.objects.filter(craftable=True).all()

    for i in items:
        try:
            update_recipe_item(i)
            sleep(0.5)
        except BaseException as e:
            logger.exception(e)

    logger.info("All items processed")


def get_recipes(item: Item, message: str, spaces: str = "") -> str:
    recipes = Recipe.objects.filter(item=item).order_by("ingredient__craftable").all()

    for r in recipes:
        message += f"{spaces}{r.amount} x {r.ingredient.name}\n"
        if r.ingredient.craftable:
            message = get_recipes(r.ingredient, message, spaces + SPACES_FOR_CRAFT_MESSAGE)

    return message


def create_message(item_command: str) -> str:
    item = Item.objects.filter(command=item_command, craftable=True).first()
    if not item:
        return "Sorry. Item not found."

    recipe = Recipe.objects.filter(item=item).first()
    if not recipe:
        return "I don't have this recipe yet. Send a message to [ricardobotsugestion](https://t.me/ricardobotsugestion)"

    dt = recipe.created_at.strftime("%b %d %Y")

    message = f"Recipe for {item.name} updated at {dt}\n\n"
    message += f"`1 x {item.name}\n"
    message = get_recipes(item, message, SPACES_FOR_CRAFT_MESSAGE)
    message += "`"
    return message
