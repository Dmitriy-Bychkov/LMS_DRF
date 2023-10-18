from celery import shared_task

from education.models import Course, Subscription


@shared_task
def subscriber_notify(course_id):
    """ Задача для уведомления подписчиков, если курс обновился """

    course = Course.objects.get(pk=course_id)  # получаем данные об измененном курсе
    subscriptions = Subscription.objects.filter(course=course_id)  # получаем подписки на данный курс

    # если подписки существуют, отправляем подписчикам курса сообщение об изменениях
    if subscriptions:
        for subscription in subscriptions:
            print(f'Уважаемый подписчик, {subscription.user}! В курсе "{course.name}" произошли недавние обновления. '
                  f'Скорее посетите наш сайт, чтобы посмотреть что изменилось в курсе!')
