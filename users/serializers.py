from rest_framework import serializers

from education.models import Payments
from education.serializers import PaymentsForOwnerSerializer
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """ Сериализотор для модели пользователей """

    # Расширяем сериализатор дополнительным вложенным полем с платежами
    payments = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = '__all__'

    # Получаем все поля для дополнительного поля платежей с фильтрацией по пользователю
    def get_payments(self, owner):
        # Если текущий пользователь не является владельцем профиля, то история платежей не отображается
        if self.context['request'].user != owner:
            return None
        return PaymentsForOwnerSerializer(Payments.objects.filter(owner=owner), many=True).data


class PublicUserSerializer(serializers.ModelSerializer):
    """ Сериализатор для публичной информации о пользователе """

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'role']
