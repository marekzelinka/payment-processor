from typing import Protocol

from pay.credit_card import CreditCard
from pay.order import Order


class PaymentProcessor(Protocol):
    def charge(self, credit_card: CreditCard, *, amount: int) -> None:
        """Charge the card."""


def pay_order(
    order: Order, payment_processor: PaymentProcessor, credit_card: CreditCard
) -> None:
    if order.total == 0:
        raise ValueError("Can't pay an order with total 0.")

    payment_processor.charge(credit_card, amount=order.total)
    order.pay()
