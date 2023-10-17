import stripe

from config import settings


def create_product(payment):
    """
    Создание продукта для оплаты через Stripe,
    попадает в личный кабинет страйпа после успешного создания
    """

    stripe.api_key = settings.STRIPE_SK

    if payment.course:
        product = stripe.Product.create(
            # Название поля и описания на платежной странице
            name='Оплата за обучение',
            description=f'Курс: {payment.course.name}',
        )
        amount = payment.course.amount
    elif payment.lesson:
        product = stripe.Product.create(
            name='Оплата за обучение',
            description=f'Урок: {payment.lesson.name}',
        )
        amount = payment.lesson.amount
    else:
        raise ValueError('Invalid Payment')

    product.save()
    price = stripe.Price.create(
        unit_amount=amount,
        # Можно указать это поле взамен, если хотим указывать свою цену (не ту что в базе данных за курс или урок)
        # unit_amount=int(payment.amount),
        currency="rub",
        # Указываем, если нужно создать периодический платеж
        # recurring={"interval": "month"},
        product=product['id'],
    )
    price.save()
    return price['id']


def get_url(price):
    """
    Получение ссылки на оплату через Stripe,
    фиксируется в личном кабинете страйпа
     """

    stripe.api_key = settings.STRIPE_SK
    # Перенаправление на страницу успешного платежа в случае успешной оплаты
    session = stripe.checkout.Session.create(
        # Здесь можно указать свою страницу с сообщением об успешном платеже
        success_url="https://example.com/success_payment",
        line_items=[
            {
                "price": price,
                "quantity": 1,
            },
        ],
        mode="payment",
    )
    return session['url']
