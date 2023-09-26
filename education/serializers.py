from rest_framework import serializers

from education.models import Course, Lesson


class CourseSerializer(serializers.ModelSerializer):
    """ Сериализотор для модели курса """

    class Meta:
        model = Course
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    """ Сериализотор для модели урока """

    class Meta:
        model = Lesson
        fields = '__all__'
