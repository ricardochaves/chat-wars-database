from chat_wars_database.app.guild_helper_bot.models import TelegramUser


def create_telegram_user_if_need(telegram_id: int, name: str, user_name: str) -> TelegramUser:

    t_u = TelegramUser.objects.filter(telegram_id=telegram_id).first()

    if t_u:
        if t_u.name != name or t_u.user_name != user_name:
            t_u.name = name
            t_u.user_name = user_name
            t_u.save()
            return t_u

        return t_u

    return TelegramUser.objects.create(telegram_id=telegram_id, name=name, user_name=user_name)
