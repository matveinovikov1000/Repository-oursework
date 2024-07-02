import json

from src.read_operations import read_operations_dataframe
from src.utils import current_date_time, greetings, spending_cards, exchange_rates, stock_price


def main_page(transactions=read_operations_dataframe("data/operations.xls"), time=current_date_time()):
    """Функция, возвращающая JSON ответ для главной страницы"""
    hello = greetings(time)
    spendings_cashback_top_five = spending_cards(transactions)
    currency = exchange_rates()
    stock = stock_price()

    hello.update(spendings_cashback_top_five)
    hello.update(currency)
    hello.update(stock)

    return json.dumps(hello, ensure_ascii=False)