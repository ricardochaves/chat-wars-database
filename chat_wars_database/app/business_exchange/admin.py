from django.contrib import admin

from chat_wars_database.app.business_exchange.models import ExchangeMessages
from chat_wars_database.app.business_exchange.models import StatsByDay


@admin.register(ExchangeMessages)
class ExchangeMessagesAdmin(admin.ModelAdmin):
    list_display = ("message_date", "message_id")


@admin.register(StatsByDay)
class StatsByDayAdmin(admin.ModelAdmin):
    list_display = ("date", "item")
