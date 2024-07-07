import json

from src.read_operations import read_operations_dataframe
from src.reports import selection_user_date
from src.utils import current_date_time, exchange_rates, greetings, spending_cards, stock_price


def main_page(
    transactions=read_operations_dataframe("data/operations.xls"),
    time=current_date_time(),
    time_sp=selection_user_date(),
):
    """Функция, возвращающая JSON ответ для главной страницы"""
    hello = greetings(time)
    spendings_cashback_top_five = spending_cards(transactions, time_sp)
    currency = exchange_rates()
    stock = stock_price()

    hello.update(spendings_cashback_top_five)
    hello.update(currency)
    hello.update(stock)

    return json.dumps(hello, ensure_ascii=False)
