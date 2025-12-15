from datetime import datetime

from pay.credit_card import CreditCard


class PaymentProcessor:
    def __init__(self, api_key: str) -> None:
        self.__api_key: str = api_key

    def charge(self, credit_card: CreditCard, *, amount: int) -> None:
        if not PaymentProcessor.validate_credit_card(credit_card):
            raise ValueError("Invalid credit card")
        if not self.__check_api_key():
            raise ValueError(f"Invalid API key: {repr(self.__api_key)}")

        print(f"Charging card number {credit_card.number} for ${amount / 100:.2f}")

    @classmethod
    def validate_credit_card(cls, credit_card: CreditCard) -> bool:
        return (
            luhn_checksum(credit_card.number)
            and datetime(credit_card.expiry_year, credit_card.expiry_month, 1)
            > datetime.now()
        )

    def __check_api_key(self) -> bool:
        return self.__api_key == "6cfb67f3-6281-4031-b893-ea85db0dce20"


def luhn_checksum(card_number: str) -> bool:
    def digits_of(card_number: str) -> list[int]:
        return [int(d) for d in card_number]

    digits = digits_of(card_number)

    checksum = 0
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum += sum(odd_digits)
    for digit in even_digits:
        checksum += sum(digits_of(str(digit * 2)))

    return checksum % 10 == 0
