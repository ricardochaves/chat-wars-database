import uuid

from django.db import models

from chat_wars_database.app.business_core.models import Item


class TelegramUser(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    user_name = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    telegram_id = models.FloatField(unique=True)

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


class Guild(models.Model):
    name = models.CharField(max_length=50, unique=True)
    captain = models.OneToOneField(TelegramUser, on_delete=models.CASCADE, unique=True)
    delete_command = models.CharField(null=True, blank=True, max_length=100)

    def __str__(self):
        return self.name


def hex_uuid():
    return uuid.uuid4().hex


class InvitationLink(models.Model):
    guild = models.ForeignKey(Guild, on_delete=models.CASCADE)
    link_id = models.UUIDField(db_index=True, default=hex_uuid)

    def __str__(self):
        return self.link_id


class UserGuild(models.Model):
    MEMBER = 1
    ADMIN = 2

    ROLES = [
        (MEMBER, "Member"),
        (ADMIN, "Admin"),
    ]

    user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE)
    guild = models.ForeignKey(Guild, on_delete=models.CASCADE)
    role = models.IntegerField(choices=ROLES, default=MEMBER)
    leave_command = models.CharField(null=True, blank=True, max_length=100)

    def __str__(self):
        return f"[{self.guild.name}] {self.user.name}"

    class Meta:
        unique_together = (
            "user",
            "guild",
        )
