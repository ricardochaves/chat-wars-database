from django.contrib import admin

from chat_wars_database.app.business_core.models import Category
from chat_wars_database.app.business_core.models import Item
from chat_wars_database.app.business_core.models import Recipe


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("command", "name")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("command", "name")


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("created_at", "item", "ingredient", "amount")
