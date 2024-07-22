import json

import pandas as pd


def read_operations_dataframe(filename="data/operations.xls"):
    """Функция, преобразующая входные данные в DataFrame"""
    reader_operations_dataframe = pd.read_excel(filename)
    return reader_operations_dataframe


def read_operations_list(filename="data/operations.xls"):
    """Функция, преобразующая входные данные в список словарей"""
    reader_operations_json = pd.read_excel(filename).to_json(orient="records", indent=4, force_ascii=False)
    reader_operations_list = list(json.loads(reader_operations_json))
    return reader_operations_list
