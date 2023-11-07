from celery import shared_task

from datetime import datetime
import pytz
import datetime

from users.models import User


@shared_task(name='user_ban')
def check_user():
    """
    Проверка пользователя на его активность:
    если пользователь не заходил в сервис более месяца, то он блокируется
    """

    users_is_active = User.objects.filter(is_active=True)

    moscow_timezone = pytz.timezone('Europe/Moscow')  # устанавливаем часовой пояс
    date_time_now = datetime.datetime.now()  # получаем текущие дату и время
    date_now = date_time_now.astimezone(moscow_timezone)  # устанавливаем текущую дату с учетом часового пояса

    # проверяем дату последнего входа пользователя
    for user in users_is_active:

        # проверяем есть ли данные о последнем входе пользователя
        if user.last_login:
            # устанавливаем дату последнего входа пользователя с учетом часового пояса
            user_last_login = user.last_login.astimezone(moscow_timezone)

            # если текущая дата больше даты последнего входа пользователя более месяца
            if (date_now.date() - user_last_login.date()).days > 30:
                # устанавливаем признак пользователя "не активен"
                user.is_active = False
                user.save()

        # если данных о последнем входе пользователя нет, заносим туда текущую дату (продлеваем ему время))
        else:
            user.last_login = date_now
            user.save()
