from datetime import date

import pytest

from pay.credit_card import CreditCard
from pay.order import LineItem, Order, OrderStatus
from pay.payment import pay_order, return_order


@pytest.fixture
def credit_card() -> CreditCard:
    year = date.today().year + 2
    return CreditCard(number="1249190007575069", expiry_month=12, expiry_year=year)


class PaymentProcessorMock:
    def charge(self, credit_card: CreditCard, *, amount: int) -> None:
        print(f"Charging card number {credit_card.number} for ${amount / 100:.2f}")

    def chargeback(self, credit_card: CreditCard, *, amount: int) -> None:
        print(
            f"Returning funds to card card with number {credit_card.number} for ${amount / 100:.2f}"
        )


def test_pay_order(credit_card: CreditCard) -> None:
    order = Order()
    order.line_items.append(LineItem(name="Shoes", price=100_00, quantity=2))
    pay_order(order, PaymentProcessorMock(), credit_card)
    assert order.status == OrderStatus.PAID


def test_pay_order_invalid(credit_card: CreditCard) -> None:
    with pytest.raises(ValueError):
        order = Order()
        pay_order(order, PaymentProcessorMock(), credit_card)


def test_chargeback_order(credit_card: CreditCard) -> None:
    order = Order()
    order.line_items.append(LineItem(name="Shoes", price=100_00, quantity=2))
    pay_order(order, PaymentProcessorMock(), credit_card)
    assert order.status == OrderStatus.PAID
    return_order(order, PaymentProcessorMock(), credit_card)
    assert order.status == OrderStatus.RETURNED
