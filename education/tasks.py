from celery import shared_task

from education.email_sender import send_mail_task
from education.models import Course, Subscription


@shared_task
def subscriber_notify(course_id):
    """ Задача для уведомления подписчиков, если курс обновился """

    course = Course.objects.get(pk=course_id)  # получаем данные об измененном курсе
    subscriptions = Subscription.objects.filter(course=course_id)  # получаем подписки на данный курс

    subject = f'Изменения в уроках вашего курса - {course.name}'

    # если подписки существуют, отправляем подписчикам курса сообщение об изменениях
    if subscriptions:
        recipient_list = []

        for subscription in subscriptions:
            message = (
                f'Уважаемый подписчик, {subscription.user}!\nВ курсе "{course.name}" произошли недавние обновления некоторых уроков.\n'
                f'Скорее посетите наш сайт, чтобы посмотреть что изменилось в курсе!')
            recipient_list.append(subscription.user.email)

        # Вызываем функцию отправки сообщения на email подписчика
        send_mail_task(subject, message, recipient_list)
