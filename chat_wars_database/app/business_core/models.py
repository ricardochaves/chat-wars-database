from django.db import models


class Item(models.Model):

    command = models.CharField(max_length=10, blank=True, null=True)
    name = models.CharField(max_length=200)  # InGameName

    tradeable_exchange = models.BooleanField(null=True, blank=True, default=None)
    tradeable_auction = models.BooleanField(null=True, blank=True, default=None)
    craftable = models.BooleanField(null=True, blank=True, default=None)
    depositable_in_guild = models.BooleanField(null=True, blank=True, default=None)
    event_item = models.BooleanField(null=True, blank=True, default=None)
    can_be_found_in_quests = models.BooleanField(null=True, blank=True, default=None)
    craft_command = models.CharField(max_length=30, null=True, blank=True)
    item_type = models.CharField(max_length=100, blank=True, null=True)
    mana_crafting = models.IntegerField(null=True, blank=True, default=None)
    skill_craft_level = models.IntegerField(null=True, blank=True, default=None)
    weight = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)

    quest_forest_day = models.BooleanField(null=True, blank=True, default=None)
    quest_swamp_day = models.BooleanField(null=True, blank=True, default=None)
    quest_valley_day = models.BooleanField(null=True, blank=True, default=None)
    quest_foray_day = models.BooleanField(null=True, blank=True, default=None)
    quest_forest_morning = models.BooleanField(null=True, blank=True, default=None)
    quest_swamp_morning = models.BooleanField(null=True, blank=True, default=None)
    quest_valley_morning = models.BooleanField(null=True, blank=True, default=None)
    quest_foray_morning = models.BooleanField(null=True, blank=True, default=None)
    quest_forest_evening = models.BooleanField(null=True, blank=True, default=None)
    quest_swamp_evening = models.BooleanField(null=True, blank=True, default=None)
    quest_valley_evening = models.BooleanField(null=True, blank=True, default=None)
    quest_foray_evening = models.BooleanField(null=True, blank=True, default=None)
    quest_forest_night = models.BooleanField(null=True, blank=True, default=None)
    quest_swamp_night = models.BooleanField(null=True, blank=True, default=None)
    quest_valley_night = models.BooleanField(null=True, blank=True, default=None)
    quest_foray_night = models.BooleanField(null=True, blank=True, default=None)
