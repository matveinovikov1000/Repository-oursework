import os
from unittest.mock import patch

import pytest
from dotenv import load_dotenv
from freezegun import freeze_time

from src.read_operations import read_operations_dataframe
from src.utils import current_date_time, exchange_rates, greetings, spending_cards, stock_price

load_dotenv()
api_key_stock = os.getenv("API_KEY_STOCK_PRICE")
api_key_rates = os.getenv("API_KEY_CURRENCY")

payload_rates = {}
headers_rates = {"apikey": api_key_rates}


@patch("requests.request")
def test_exchange_rates(mock_rates):
    mock_rates.return_value.json.return_value = {
        "base": "RUB",
        "date": "2021-03-17",
        "rates": {
            "USD": 0.813399,
            "EUR": 0.72007,
        },
        "success": True,
        "timestamp": 1519296206,
    }
    assert exchange_rates() == {
        "currency_rates": [
            {"currency": "USD", "rate": round(1 / 0.813399, 4)},
            {"currency": "EUR", "rate": round(1 / 0.72007, 4)},
        ]
    }
    mock_rates.assert_called_once_with(
        "GET",
        f"https://api.apilayer.com/exchangerates_data/latest?symbols={"USD"},{"EUR"}&base={"RUB"}",
        headers=headers_rates,
        data=payload_rates,
    )


@patch("requests.get")
def test_stock_price(mock_stock):
    mock_stock.return_value.json.return_value = {
        "Global Quote": {
            "01. symbol": "AAPL",
            "02. open": "174.8400",
            "03. high": "177.4850",
            "04. low": "174.3200",
            "05. price": "177.3000",
            "06. volume": "2883275",
            "07. latest trading day": "2024-07-02",
            "08. previous close": "175.1000",
            "09. change": "2.2000",
            "10. change percent": "1.2564%",
        }
    }
    assert stock_price() == {
        "stock_prices": [{"stock": "AAPL", "price": "177.3000"}, {"stock": "AAPL", "price": "177.3000"}]
    }


@pytest.mark.parametrize(
    "str_date, required_result",
    [
        ("2024-07-07 04:00:00", {"greeting": "Доброй ночи"}),
        ("2024-07-07 08:00:00", {"greeting": "Доброе утро"}),
        ("2024-07-07 13:00:00", {"greeting": "Добрый день"}),
        ("2024-07-07 20:00:00", {"greeting": "Добрый вечер"}),
    ],
)
def test_greetings(str_date, required_result):
    assert greetings(str_date) == required_result


@freeze_time("2023-01-01")
def test_current_date_time():
    assert current_date_time() == "2023-01-01 00:00:00"


def test_spending_cards():
    assert spending_cards(read_operations_dataframe(filename="operations_test.xls"), "21.12.2021") == {
        "cards": [
            {"last_digits": "*4556", "total_spent": -1252.9, "cashback": 44.0},
            {"last_digits": "*5091", "total_spent": -12054.47, "cashback": 0.0},
            {"last_digits": "*7197", "total_spent": -14720.01, "cashback": 0.0},
        ],
        "top_transactions": [
            {"date": "16.12.2021", "amount": -14216.42, "category": "ЖКХ", "description": "ЖКУ Квартира"},
            {"date": "02.12.2021", "amount": -5510.8, "category": "Каршеринг", "description": "Ситидрайв"},
            {"date": "14.12.2021", "amount": -5000.0, "category": "Переводы", "description": "Светлана Т."},
            {"date": "04.12.2021", "amount": -3499.0, "category": "Электроника и техника", "description": "DNS"},
            {"date": "21.12.2021", "amount": -1400.0, "category": "Дом и ремонт", "description": "YM*o481"},
        ],
    }
    assert (
        spending_cards(read_operations_dataframe(filename="operations_test.xls"), "07.07.2023")
        == "За указанный период транзакции не найдены"
    )
