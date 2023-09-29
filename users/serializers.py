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
        return PaymentsForOwnerSerializer(Payments.objects.filter(owner=owner), many=True).data
