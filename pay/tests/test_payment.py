from datetime import datetime

from pytest import MonkeyPatch, raises

from pay.order import LineItem, Order
from pay.payment import pay_order
from pay.processor import PaymentProcessor


def test_pay_order(monkeypatch: MonkeyPatch) -> None:
    current_year = datetime.now().year
    future_year = current_year + 12
    inputs = ["1249190007575069", "12", str(future_year)]
    monkeypatch.setattr("builtins.input", lambda _: inputs.pop(0))
    monkeypatch.setattr(PaymentProcessor, "_check_api_key", lambda _: True)
    order = Order()
    order.line_items.append(LineItem(name="Shoes", price=100_00, quantity=2))
    pay_order(order)


def test_pay_order_invalid(monkeypatch: MonkeyPatch) -> None:
    with raises(ValueError):
        current_year = datetime.now().year
        future_year = current_year + 12
        inputs = ["1249190007575069", "12", str(future_year)]
        monkeypatch.setattr("builtins.input", lambda _: inputs.pop(0))
        monkeypatch.setattr(PaymentProcessor, "_check_api_key", lambda _: True)
        order = Order()
        pay_order(order)
