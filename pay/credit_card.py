from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True)
class CreditCard:
    number: str
    expiry_month: int
    expiry_year: int
