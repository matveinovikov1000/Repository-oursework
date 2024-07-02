from unittest.mock import patch
from src.utils import exchange_rates


@patch('requests.request')
def test_exchange_rates(mock_rates):
    mock_rates.return_value.json.return_value = {
      "base": "RUB",
      "date": "2021-03-17",
      "rates": {
        "USD": 0.813399,
        "EUR": 0.72007,
      },
      "success": True,
      "timestamp": 1519296206
    }
    assert exchange_rates() == {"currency_rates": [{"currency": "USD", "rate": round(1/0.813399, 4)},
                                   {"currency": "EUR", "rate": round(1/0.72007, 4)}]}
