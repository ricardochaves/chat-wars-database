from django.db import models

from chat_wars_database.app.business_core.models import Item


class TelegramUser(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    user_name = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    telegram_id = models.FloatField()

    def __str__(self):
        return self.name


class Message(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    chat_id = models.FloatField()
    forward_date = models.DateTimeField()
    telegram_user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE)
    message_text = models.TextField()
    message_id = models.FloatField()

    def __str__(self):
        return f"{self.telegram_user.name} - {self.message_id}"


class UserDeposits(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    telegram_user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    total = models.IntegerField()

    def __str__(self):
        return f"{self.telegram_user.name} - {self.item.name} - {self.total}"
