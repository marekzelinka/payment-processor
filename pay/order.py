from dataclasses import dataclass, field
from enum import Enum


# TODO: StrEnum
class OrderStatus(Enum):
    OPEN = "open"
    PAID = "paid"


# TODO: make fronzen, kw only
@dataclass
class LineItem:
    name: str
    # TODO: price could be float
    price: int
    quantity: int = 1

    @property
    def total(self) -> int:
        return self.price * self.quantity


# TODO: make fronzen, kw only
@dataclass
class Order:
    line_items: list[LineItem] = field(default_factory=list)
    status: OrderStatus = OrderStatus.OPEN

    @property
    def total(self) -> int:
        # TODO: use sum(map(...
        return sum(item.total for item in self.line_items)

    def pay(self) -> None:
        self.status = OrderStatus.PAID
