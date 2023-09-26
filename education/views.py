from rest_framework import viewsets, generics

from education.models import Course, Lesson
from education.serializers import CourseSerializer, LessonSerializer


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
