import datetime
import json
import logging
import os

import pandas as pd
import requests
from dotenv import load_dotenv

logger_ut = logging.getLogger(__name__)
file_handler_ut = logging.StreamHandler()
file_formatter_ut = logging.Formatter("%(asctime)s %(filename)s %(levelname)s: %(message)s")
file_handler_ut.setFormatter(file_formatter_ut)
logger_ut.addHandler(file_handler_ut)
logger_ut.setLevel(logging.DEBUG)


def current_date_time():
    """Возвращает текущие дату и время в формате YYYY-MM-DD HH:MM:SS"""
    date_time = datetime.datetime.now()
    date_time_str = date_time.strftime("%Y-%m-%d %H:%M:%S")
    logger_ut.info("Вывод текущей даты/времени в str")
    return date_time_str


def greetings(time=current_date_time):
    """Приветствие в соответсвии с текущим временем"""
    logger_ut.info("Преобразование времени из str в datetime + обращение к атрибуту часа")
    time_obj = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
    hour_obj = time_obj.hour
    greetings_str = " "

    logger_ut.info("Выбор приветствия в соответсвии с текущим временем")
    if hour_obj >= 23 or hour_obj <= 5:
        greetings_time_day = greetings_str.replace(" ", "Доброй ночи")
    elif 6 <= hour_obj <= 10:
        greetings_time_day = greetings_str.replace(" ", "Доброе утро")
    elif 11 <= hour_obj <= 17:
        greetings_time_day = greetings_str.replace(" ", "Добрый день")
    elif 18 <= hour_obj <= 22:
        greetings_time_day = greetings_str.replace(" ", "Добрый вечер")

    logger_ut.info("Запись приветствия в словарь")
    greetings_time_day_dict = {"greeting": f"{greetings_time_day}"}

    return greetings_time_day_dict


def spending_cards(transactions, time_sp):
    """Функция, показывающая сумму расходов и кэшбек за период по каждой карте + ТОП-5 транзакций по сумме платежа"""
    user_date_obj = datetime.datetime.strptime(time_sp, "%d.%m.%Y")
    data = transactions.to_json(orient="records", indent=4, force_ascii=False)
    data_py = json.loads(data)
    period_list = []
    spending_list = []
    top_five_list = []
    sum_cards_list = []

    for transaction in data_py:
        try:
            logger_ut.info("Перебор транзакций для фильтрации по периоду")
            data_obj = datetime.datetime.strptime(transaction["Дата платежа"], "%d.%m.%Y")
            if (
                data_obj.day <= user_date_obj.day
                and data_obj.month == user_date_obj.month
                and data_obj.year == user_date_obj.year
            ):
                period_list.append(transaction)
        except TypeError:
            logger_ut.warning("Ключ не найден")
            pass

    for spending in period_list:
        logger_ut.info("Фильтр списка транзакций по тратам")
        if spending["Сумма платежа"] < 0:
            spending_list.append(spending)

    try:
        logger_ut.info("Обработка таблицы для получения трат и кэшбэка по картам")
        df_spending = pd.DataFrame(spending_list)
        numbers_card_spending_grouped = df_spending.groupby("Номер карты")
        sum_spending = numbers_card_spending_grouped["Сумма платежа"].sum().reset_index()
        sum_cashback = numbers_card_spending_grouped["Кэшбэк"].sum().reset_index()
        sum_spending["Кэшбэк"] = sum_cashback["Кэшбэк"]
        data_sum_cards_json = sum_spending.to_json(orient="records", indent=4, force_ascii=False)
        data_sum_cards_py = json.loads(data_sum_cards_json)

        for sum_card in data_sum_cards_py:
            logger_ut.info("Запись результата в список")
            sum_card_dict = {
                "last_digits": sum_card.get("Номер карты"),
                "total_spent": sum_card.get("Сумма платежа"),
                "cashback": sum_card.get("Кэшбэк"),
            }
            sum_cards_list.append(sum_card_dict)

        logger_ut.info("Обработка таблицы для получения ТОП-5 трат по картам")
        top_five_transaction = df_spending.sort_values("Сумма платежа").head()
        data_top = top_five_transaction.to_json(orient="records", indent=4, force_ascii=False)
        data_top_py = json.loads(data_top)

        for top in data_top_py:
            logger_ut.info("Запись результата в список")
            top_five = {
                "date": top.get("Дата платежа"),
                "amount": top.get("Сумма платежа"),
                "category": top.get("Категория"),
                "description": top.get("Описание"),
            }
            top_five_list.append(top_five)

        return {"cards": sum_cards_list, "top_transactions": top_five_list}

    except KeyError:
        logger_ut.warning("Ключ не найден")
        return "За указанный период транзакции не найдены"


def exchange_rates():
    """Функция, возвращающая курсы валют"""
    logger_ut.info("Чтение файла с заданными параметрами")
    with open("user_settings.json") as file:
        user_sett = json.load(file)

    user_currency = user_sett["user_currencies"]

    load_dotenv()
    api_key = os.getenv("API_KEY_CURRENCY")

    url = (f"https://api.apilayer.com/exchangerates_data/"
           f"latest?symbols={user_currency[0]},{user_currency[1]}&base={"RUB"}")

    payload = {}
    headers = {"apikey": api_key}

    logger_ut.info("Обращение к API")
    response = requests.request("GET", url, headers=headers, data=payload)

    result_py = response.json()

    logger_ut.info("Запись ответа от API в словарь")
    data_rate = {
        "currency_rates": [
            {"currency": "USD", "rate": round(1 / result_py["rates"]["USD"], 4)},
            {"currency": "EUR", "rate": round(1 / result_py["rates"]["EUR"], 4)},
        ]
    }

    return data_rate


def stock_price():
    """Функция, возвращающая стоимость ценных бумаг"""
    logger_ut.info("Чтение файла с заданными параметрами")
    with open("user_settings.json") as file:
        user_sett = json.load(file)

    user_stock = user_sett["user_stocks"]

    load_dotenv()
    api_key = os.getenv("API_KEY_STOCK_PRICE")

    logger_ut.info("Обращение к API")
    url_aapl = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={user_stock[0]}&apikey={api_key}"
    url_amzn = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={user_stock[1]}&apikey={api_key}"

    r_aapl = requests.get(url_aapl)
    data_aapl = r_aapl.json()

    r_amzn = requests.get(url_amzn)
    data_amzn = r_amzn.json()

    logger_ut.info("Запись ответа от API в словарь")
    data_stock = {
        "stock_prices": [
            {"stock": data_aapl["Global Quote"]["01. symbol"], "price": data_aapl["Global Quote"]["05. price"]},
            {"stock": data_amzn["Global Quote"]["01. symbol"], "price": data_amzn["Global Quote"]["05. price"]},
        ]
    }

    return data_stock
