from django.db import models


class Category(models.Model):

    command = models.CharField(max_length=10, blank=True, null=True)
    name = models.CharField(max_length=200)


class Item(models.Model):

    command = models.CharField(max_length=10, blank=True, null=True)
    name = models.CharField(max_length=200)  # InGameName

    tradeable_exchange = models.BooleanField(null=True, blank=True)
    tradeable_auction = models.BooleanField(null=True, blank=True)
    craftable = models.BooleanField(null=True, blank=True)
    depositable_in_guild = models.BooleanField(null=True, blank=True)
    event_item = models.BooleanField(null=True, blank=True)
    can_be_found_in_quests = models.BooleanField(null=True, blank=True)
    craft_command = models.CharField(max_length=30, null=True, blank=True)
    mana_crafting = models.IntegerField(null=True, blank=True)
    skill_craft_level = models.IntegerField(null=True, blank=True)
    weight = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    modification_date = models.DateTimeField(null=True, blank=True)
    base_duration = models.IntegerField(null=True, blank=True)

    categories = models.ManyToManyField(Category)

    # PotionEffect
    # SkillCraft
    # Note - We can use it to ask for help and enrich the base.

    quest_forest_day = models.BooleanField(null=True, blank=True)
    quest_swamp_day = models.BooleanField(null=True, blank=True)
    quest_valley_day = models.BooleanField(null=True, blank=True)
    quest_foray_day = models.BooleanField(null=True, blank=True)
    quest_forest_morning = models.BooleanField(null=True, blank=True)
    quest_swamp_morning = models.BooleanField(null=True, blank=True)
    quest_valley_morning = models.BooleanField(null=True, blank=True)
    quest_foray_morning = models.BooleanField(null=True, blank=True)
    quest_forest_evening = models.BooleanField(null=True, blank=True)
    quest_swamp_evening = models.BooleanField(null=True, blank=True)
    quest_valley_evening = models.BooleanField(null=True, blank=True)
    quest_foray_evening = models.BooleanField(null=True, blank=True)
    quest_forest_night = models.BooleanField(null=True, blank=True)
    quest_swamp_night = models.BooleanField(null=True, blank=True)
    quest_valley_night = models.BooleanField(null=True, blank=True)
    quest_foray_night = models.BooleanField(null=True, blank=True)
