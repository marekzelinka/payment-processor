import os

import pyinputplus as pyip
from dotenv import load_dotenv

from pay.credit_card import CreditCard
from pay.order import LineItem, Order
from pay.payment import pay_order
from pay.payment_processor import PaymentProcessor


# Test card number: 1249190007575069
def input_card_info() -> CreditCard:
    card = pyip.inputStr("Please enter your card number: ", strip=True, limit=16)
    month = pyip.inputInt("Please enter the card expiry month: ", min=1, max=12)
    year = pyip.inputInt("Please enter the card expiry year: ", greaterThan=0)

    return CreditCard(number=card, expiry_month=month, expiry_year=year)


def main() -> None:
    load_dotenv()
    API_KEY = os.getenv("api_key") or ""
    payment_processor = PaymentProcessor(API_KEY)

    order = Order()
    order.line_items.append(LineItem(name="Shoes", price=100_00, quantity=2))
    order.line_items.append(LineItem(name="Hat", price=50_00))

    # read card info from user
    credit_card = input_card_info()
    pay_order(order, payment_processor, credit_card)


if __name__ == "__main__":
    main()
