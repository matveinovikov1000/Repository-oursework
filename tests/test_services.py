import json

from src.services import search_transfers_individuals


def test_search_transfers_individuals(fixt_list):
    assert search_transfers_individuals(fixt_list) == json.dumps(
        [
            {
                "Категория": "Переводы",
                "Описание": "Константин Л.",
                "Покупки пн": "Картошка",
                "Покупки вт": "Хлеб",
                "Покупки ср": "Молоко",
                "Покупки чт": "Сыр",
                "Покупки пт": "Масло",
            }
        ],
        ensure_ascii=False,
    )
