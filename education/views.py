from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import OrderingFilter
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated

from education.models import Course, Lesson, Payments, Subscription
from education.paginators import EducationPaginator
from education.permissions import IsModeratorOrReadOnly, IsCourseOrLessonOwner, IsPaymentOwner, IsCourseOwner
from education.serializers import CourseSerializer, LessonSerializer, PaymentsSerializer, SubscriptionSerializer, \
    PaymentCreateSerializer
from users.helpers import is_moderator

from education.tasks import subscriber_notify


class CourseViewSet(viewsets.ModelViewSet):
    """ ViewSet - набор для основных CRUD - действий над курсами """

    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsModeratorOrReadOnly | IsCourseOwner]
    pagination_class = EducationPaginator

    def get_queryset(self):
        """ Переопределяем queryset, чтобы доступ к обьекту имели только его владельцы и модератор """

        if self.request.user.is_anonymous:
            return Course.objects.none()
        if is_moderator(self.request.user):
            return Course.objects.all()
        else:
            return Course.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        """ Переопределяем метод создания обьекта с условием, чтобы модераторы не могли создавать обьект """

        if is_moderator(self.request.user):
            raise PermissionDenied("Вы не можете создавать новые курсы!")
        else:
            new_payment = serializer.save()
            new_payment.owner = self.request.user
            new_payment.save()

    def perform_destroy(self, instance):
        """ Переопределяем метод удаления обьекта с условием, чтобы модераторы не могли удалять обьект """

        if is_moderator(self.request.user):
            raise PermissionDenied("Вы не можете удалять курсы!")
        instance.delete()


class LessonCreateAPIView(generics.CreateAPIView):
    """ Generic - класс для создания нового урока """

    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModeratorOrReadOnly | IsCourseOrLessonOwner]

    def perform_create(self, serializer):
        """ Переопределяем метод создания обьекта с условием, чтобы модераторы не могли создавать обьект """

        if is_moderator(self.request.user):
            raise PermissionDenied("Вы не можете создать новый урок!")
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()

        # запускаем отложенную задачу по информированию подписчиков курса о добалении нового урока
        subscriber_notify.delay(new_lesson.course_id)


class LessonListAPIView(generics.ListAPIView):
    """ Generic - класс для вывода списка уроков """

    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModeratorOrReadOnly | IsCourseOrLessonOwner]
    pagination_class = EducationPaginator

    def get_queryset(self):
        """ Переопределяем queryset чтобы доступ к обьекту имели только его владельцы и модератор """

        if self.request.user.is_anonymous:
            return Lesson.objects.none()
        if is_moderator(self.request.user):
            return Lesson.objects.all()
        else:
            return Lesson.objects.filter(owner=self.request.user)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """ Generic - класс для просмотра урока """

    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModeratorOrReadOnly | IsCourseOrLessonOwner]

    def get_queryset(self):
        """ Переопределяем queryset чтобы доступ к обьекту имели только его владельцы и модератор """

        if self.request.user.is_anonymous:
            return Lesson.objects.none()
        if is_moderator(self.request.user):
            return Lesson.objects.all()
        else:
            return Lesson.objects.filter(owner=self.request.user)


class LessonUpdateAPIView(generics.UpdateAPIView):
    """ Generic - класс для изменения (редактирования) урока """

    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModeratorOrReadOnly | IsCourseOrLessonOwner]

    def get_queryset(self):
        """ Переопределяем queryset чтобы доступ к обьекту имели только его владельцы и модератор """

        if self.request.user.is_anonymous:
            return Lesson.objects.none()
        if is_moderator(self.request.user):
            return Lesson.objects.all()
        else:
            return Lesson.objects.filter(owner=self.request.user)

    def perform_update(self, serializer):
        """ Переопределяем метод изменения урока """

        changed_lesson = serializer.save()
        changed_lesson.save()

        # запускаем отложенную задачу по информированию подписчиков курса о изменениях уроков курса
        subscriber_notify.delay(changed_lesson.course_id)


class LessonDestroyAPIView(generics.DestroyAPIView):
    """ Generic - класс для удаления урока """

    permission_classes = [IsAuthenticated, IsModeratorOrReadOnly | IsCourseOrLessonOwner]

    def get_queryset(self):
        """ Переопределяем queryset чтобы доступ к обьекту имели только его владельцы и модератор """

        if self.request.user.is_anonymous:
            return Lesson.objects.none()
        if is_moderator(self.request.user):
            return Lesson.objects.all()
        else:
            return Lesson.objects.filter(owner=self.request.user)

    def perform_destroy(self, instance):
        """ Переопределяем метод удаления обьекта с условием, чтобы модераторы не могли удалять обьект """

        if is_moderator(self.request.user):
            raise PermissionDenied("Вы не можете удалять уроки!")
        instance.delete()


class PaymentsCreateAPIView(generics.CreateAPIView):
    """ Generic - класс для создания нового платежа """

    serializer_class = PaymentCreateSerializer
    permission_classes = [IsAuthenticated, IsPaymentOwner]

    def perform_create(self, serializer):
        """ Переопределяем метод создания обьекта с условием, чтобы модераторы не могли создавать обьект """

        if is_moderator(self.request.user):
            raise PermissionDenied("Вы не можете создавать новые платежи!")
        else:
            new_payment = serializer.save()
            new_payment.owner = self.request.user
            new_payment.save()


class PaymentsListAPIView(generics.ListAPIView):
    """ Generic - класс для вывода списка платежей """

    serializer_class = PaymentsSerializer
    permission_classes = [IsAuthenticated, IsModeratorOrReadOnly | IsPaymentOwner]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    # Определяем фильтрацию по нужным нам полям
    filterset_fields = ('course', 'lesson', 'owner', 'payment_method',)
    # Определяем фильтрацию по дате
    ordering_fields = ('payment_date',)

    def get_queryset(self):
        """ Переопределяем queryset чтобы доступ к обьекту имели только его владельцы и модератор """

        if self.request.user.is_anonymous:
            return Payments.objects.none()
        if is_moderator(self.request.user):
            return Payments.objects.all()
        else:
            return Payments.objects.filter(owner=self.request.user)


class PaymentsRetrieveAPIView(generics.RetrieveAPIView):
    """ Generic - класс для просмотра платежа """

    serializer_class = PaymentsSerializer
    permission_classes = [IsAuthenticated, IsModeratorOrReadOnly | IsPaymentOwner]

    def get_queryset(self):
        """ Переопределяем queryset чтобы доступ к обьекту имели только его владельцы и модератор """

        if self.request.user.is_anonymous:
            return Payments.objects.none()
        if is_moderator(self.request.user):
            return Payments.objects.all()
        else:
            return Payments.objects.filter(owner=self.request.user)


class SubscriptionViewSet(viewsets.ModelViewSet):
    """ ViewSet - набор основных CRUD действий над подписками на курсы """

    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()
    lookup_field = 'id'

    def perform_create(self, serializer):
        """ Переопределение метода создания подписки, чтобы сохранять текущий статус подписки True или False """

        new_subscription = serializer.save(user=self.request.user)  # Сохраняем связь пользователя
        new_subscription.save()
