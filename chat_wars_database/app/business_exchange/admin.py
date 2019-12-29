from django.contrib import admin

from chat_wars_database.app.business_exchange.models import ExchangeMessages


@admin.register(ExchangeMessages)
class ExchangeMessagesAdmin(admin.ModelAdmin):
    list_display = ("message_date", "message_id")
