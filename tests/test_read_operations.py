from src.read_operations import read_operations_dataframe, read_operations_list


def test_read_operations_list():
    assert read_operations_list(filename="test_operations.xlsx") == [
        {
            "Покупки сб": "Билет в кино",
            "Покупки вс": "Вода",
            "Покупки пн": "Картошка",
            "Покупки вт": "Хлеб",
            "Покупки ср": "Молоко",
            "Покупки чт": "Сыр",
            "Покупки пт": "Масло",
        }
    ]


def test_read_operations_dataframe():
    assert read_operations_dataframe(filename="test_operations.xlsx").any
