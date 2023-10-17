from django.conf import settings
from django.db import models
from django.utils import timezone

NULLABLE = {'blank': True, 'null': True}


class Course(models.Model):
    """ Создание модели для курса - полей курсов в таблице БД """

    name = models.CharField(max_length=100, verbose_name='название курса')
    preview = models.ImageField(upload_to='courses/', verbose_name='изображение курса', **NULLABLE)
    description = models.TextField(verbose_name='описание курса')
    amount = models.PositiveIntegerField(default=0, verbose_name='цена')

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='владелец курса',
                              **NULLABLE)

    def __str__(self):
        return f'{self.name}, {self.description}, {self.preview}'

    class Meta:
        """ Представление написания заголовков в админке """

        verbose_name = "курс"
        verbose_name_plural = "курсы"


class Lesson(models.Model):
    """ Создание модели для урока - полей уроков в таблице БД """

    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс')
    name = models.CharField(max_length=100, verbose_name='название урока')
    description = models.TextField(verbose_name='описание урока')
    preview = models.ImageField(upload_to='lessons/', verbose_name='изображение урока', **NULLABLE)
    video_url = models.URLField(verbose_name='ссылка на видео урока', **NULLABLE)
    amount = models.PositiveIntegerField(default=0, verbose_name='цена')

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='владелец урока',
                              **NULLABLE)

    def __str__(self):
        return f'{self.name}, {self.description}, {self.preview}'

    class Meta:
        """ Представление написания заголовков в админке """

        verbose_name = "урок"
        verbose_name_plural = "уроки"


class Payments(models.Model):
    """ Создание модели для платежей - полей платежей в таблице БД """

    PAYMENT_METHODS = (
        ('cash', 'Наличные'),
        ('transfer', 'Перевод на счет'),
    )

    course = models.ForeignKey(Course, on_delete=models.CASCADE, **NULLABLE, related_name='payments')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, **NULLABLE, related_name='payments')

    payment_date = models.DateTimeField(default=timezone.now, verbose_name='дата оплаты')
    amount = models.IntegerField(verbose_name='сумма оплаты', **NULLABLE)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, verbose_name='способ оплаты',
                                      default='transfer')

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='владелец платежа',
                              related_name='payment_user', **NULLABLE)

    def __str__(self):
        return f'{self.lesson if self.lesson else self.course} - {self.amount}'

    class Meta:
        """ Представление написания заголовков в админке """

        verbose_name = 'платеж'
        verbose_name_plural = 'платежи'


class Subscription(models.Model):
    """ Модель подписки пользователя на обновления курса """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             verbose_name="пользователь подписки", )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс', **NULLABLE)
    is_subscribed = models.BooleanField(default=False, verbose_name='статус подписки')

    def __str__(self):
        return f"{self.user} - {self.course}"

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
