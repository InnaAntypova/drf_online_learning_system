import os
import stripe


def create_product(name: str):
    """ Создание Product (Продукта) в API stripe.com для работы с платежами """
    stripe.api_key = os.getenv('STRIPE_KEY')
    product = stripe.Product.create(name=name)
    return product


def create_payment(amount: int, product_id: str, email: str):
    """ Создание Price (Цена) и Session (Сессии) в API stripe.com для работы с платежами """
    stripe.api_key = os.getenv('STRIPE_KEY')
    price = stripe.Price.create(
        currency="rub",
        unit_amount=amount * 100,
        product_data={"name": f"{product_id}"},
    )
    session = stripe.checkout.Session.create(
        success_url="https://example.com/success",
        line_items=[{"price": f"{price['id']}", "quantity": 1}],
        mode="payment",
        customer_email=f"{email}"
    )
    return session


def get_status(session_id: str):
    """ Проверка статуса платежа """
    stripe.api_key = os.getenv('STRIPE_KEY')
    payment = stripe.checkout.Session.retrieve(
                f"{session_id}",
                )
    return payment["payment_status"]


def delete_product(name: str):
    """ Удаление Product из API stripe.com """
    stripe.api_key = os.getenv('STRIPE_KEY')
    stripe.Product.delete(f"{name}")
