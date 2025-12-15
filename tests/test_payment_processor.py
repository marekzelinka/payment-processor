import os
from datetime import date

import pytest
from dotenv import load_dotenv

from pay.credit_card import CreditCard
from pay.payment_processor import PaymentProcessor, luhn_checksum

load_dotenv()
API_KEY = os.getenv("api_key") or ""

CC_YEAR = date.today().year + 2


@pytest.fixture
def payment_processor() -> PaymentProcessor:
    return PaymentProcessor(API_KEY)


def test_invalid_api_key() -> None:
    with pytest.raises(ValueError):
        valid_credit_card = CreditCard(
            number="1249190007575069", expiry_month=12, expiry_year=CC_YEAR
        )
        INVALID_API_KEY = ""
        PaymentProcessor(INVALID_API_KEY).charge(valid_credit_card, amount=100)


def test_card_number_valid_date() -> None:
    valid_credit_card = CreditCard(
        number="1249190007575069", expiry_month=12, expiry_year=CC_YEAR
    )
    assert PaymentProcessor.validate_credit_card(valid_credit_card)


def test_card_number_invalid_date() -> None:
    credit_card = CreditCard(
        number="1249190007575069", expiry_month=12, expiry_year=1900
    )
    assert not PaymentProcessor.validate_credit_card(credit_card)


def test_card_number_invalid_luhn() -> None:
    assert not luhn_checksum("1249190007575068")


def test_card_number_valid_luhn() -> None:
    assert luhn_checksum("1249190007575069")


def test_charge_card_valid(payment_processor: PaymentProcessor) -> None:
    valid_credit_card = CreditCard(
        number="1249190007575069", expiry_month=12, expiry_year=CC_YEAR
    )
    payment_processor.charge(valid_credit_card, amount=100)


def test_charge_card_invalid(payment_processor: PaymentProcessor) -> None:
    with pytest.raises(ValueError):
        invalid_credit_card = CreditCard(
            number="1249190007575068", expiry_month=12, expiry_year=1990
        )
        payment_processor.charge(invalid_credit_card, amount=100)
