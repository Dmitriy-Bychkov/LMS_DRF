from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework import generics, viewsets

from education.models import Course, Lesson, Payments
from education.serializers import CourseSerializer, LessonSerializer, PaymentsSerializer


class CourseViewSet(viewsets.ModelViewSet):
    """ ViewSet - набор для основных CRUD - действий над курсами """

    serializer_class = CourseSerializer
    queryset = Course.objects.all()


class LessonCreateAPIView(generics.CreateAPIView):
    """ Generic - класс для создания нового урока """

    serializer_class = LessonSerializer


class LessonListAPIView(generics.ListAPIView):
    """ Generic - класс для вывода списка уроков """

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """ Generic - класс для просмотра урока """

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonUpdateAPIView(generics.UpdateAPIView):
    """ Generic - класс для изменения (редактирования) урока """

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonDestroyAPIView(generics.DestroyAPIView):
    """ Generic - класс для удаления урока """

    queryset = Lesson.objects.all()


class PaymentsListAPIView(generics.ListAPIView):
    """ Generic - класс для вывода списка платежей """

    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    # Определяем фильтрацию по нужным нам полям
    filterset_fields = ('course', 'lesson', 'owner', 'payment_method',)
    # Определяем фильтрацию по дате
    ordering_fields = ('payment_date',)


class PaymentsRetrieveAPIView(generics.RetrieveAPIView):
    """ Generic - класс для просмотра платежа """

    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()
