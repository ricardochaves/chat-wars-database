from django.contrib import admin

from chat_wars_database.app.business_core.models import Category
from chat_wars_database.app.business_core.models import Item


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("command", "name")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("command", "name")
