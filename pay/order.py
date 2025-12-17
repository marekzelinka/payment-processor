from dataclasses import dataclass, field
from enum import StrEnum, auto


class OrderStatus(StrEnum):
    OPEN = auto()
    PAID = auto()
    RETURNED = auto()


@dataclass(kw_only=True)
class LineItem:
    name: str
    price: int
    quantity: int = 1

    @property
    def total(self) -> int:
        return self.price * self.quantity


@dataclass(kw_only=True)
class Order:
    line_items: list[LineItem] = field(default_factory=list)
    status: OrderStatus = OrderStatus.OPEN

    @property
    def total(self) -> int:
        return sum(item.total for item in self.line_items)

    def add_to_delivery(self, item: LineItem) -> None:
        self.line_items.append(item)

    def pay(self) -> None:
        self.status = OrderStatus.PAID

    def returned(self) -> None:
        self.status = OrderStatus.RETURNED
