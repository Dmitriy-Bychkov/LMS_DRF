from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from education.models import Course, Lesson, Payments, Subscription
from education.validators import UrlValidator
from users.models import User


class LessonSerializer(serializers.ModelSerializer):
    """ Сериализотор для модели урока """

    # Выводим название курса в поле "course", вместо цифры
    course = SlugRelatedField(slug_field='name', queryset=Course.objects.all())

    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [
            UrlValidator(fields=['name', 'description', 'video_url']),
            serializers.UniqueTogetherValidator(fields=['name', 'description'], queryset=Lesson.objects.all())
        ]


class LessonListSerializer(serializers.ModelSerializer):
    """ Сериализотор для модели урока для использования его в выводе в курсах """

    class Meta:
        model = Lesson
        fields = ['id', 'name', 'description', 'preview', 'video_url']


class CourseSerializer(serializers.ModelSerializer):
    """ Сериализотор для модели курса """

    # Выводим счетчик уроков
    lessons_count = serializers.IntegerField(source='lesson_set.count', read_only=True)
    # Расширяем сериализатор дополнительным вложенным полем с уроками
    lessons = serializers.SerializerMethodField()
    # Расширяем сериализатор дополнительным вложенным полем со статусом подписки
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    # Выводим имя пользователя в поле "owner", вместо цифры
    owner = SlugRelatedField(slug_field='first_name', queryset=User.objects.all())

    class Meta:
        model = Course
        fields = '__all__'
        validators = [
            UrlValidator(fields=['name', 'description']),
            serializers.UniqueTogetherValidator(fields=['name', 'description'], queryset=Course.objects.all())
        ]

    # Получаем все поля для дополнительного поля уроков с фильтрацией по курсу
    def get_lessons(self, course):
        return LessonListSerializer(Lesson.objects.filter(course=course), many=True).data

    # Получаем поле статуса подписки с фильтрацией по пользователю подписки
    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        return Subscription.objects.filter(user=user, course=obj).exists()


class PaymentsSerializer(serializers.ModelSerializer):
    """ Сериализотор для модели платежей """

    # Выводим название курса в поле "course", вместо цифры
    course = SlugRelatedField(slug_field='name', queryset=Course.objects.all())
    # Выводим название урока в поле "lesson", вместо цифры
    lesson = SlugRelatedField(slug_field='name', queryset=Lesson.objects.all())
    # Выводим имя пользователя в поле "owner", вместо цифры
    owner = SlugRelatedField(slug_field='first_name', queryset=User.objects.all())

    class Meta:
        model = Payments
        fields = '__all__'


class PaymentsForOwnerSerializer(serializers.ModelSerializer):
    """ Сериализотор для модели платежей для использования его в выводе у пользователей """

    class Meta:
        model = Payments
        fields = ['id', 'amount', 'payment_date', 'payment_method']


class SubscriptionSerializer(serializers.ModelSerializer):
    """ Сериализотор для модели подписки пользователя на курс """

    class Meta:
        model = Subscription
        fields = '__all__'
