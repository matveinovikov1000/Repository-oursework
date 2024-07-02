import json
import re
import logging
from src.read_operations import read_operations_list

logger_ser = logging.getLogger(__name__)
file_handler_ser = logging.StreamHandler()
file_formatter_ser = logging.Formatter("%(asctime)s %(filename)s %(levelname)s: %(message)s")
file_handler_ser.setFormatter(file_formatter_ser)
logger_ser.addHandler(file_handler_ser)
logger_ser.setLevel(logging.DEBUG)


def search_transfers_individuals(read_operations_list):
    """Функция для поиска переводов физическим лицам"""
    logger_ser.info("Чтение файла с операциями")
    data_py = read_operations_list(filename="data/operations.xls")
    data_transfers = []

    for transaction in data_py:
        try:
            logger_ser.info("Выбор операций перевода по необходимому паттерну")
            match = re.search(r"\w+\s+\D\.", transaction["Описание"])
            if transaction["Категория"] == "Переводы" and match:
                data_transfers.append(transaction)
        except KeyError:
            logger_ser.warning("Ключ не найден")
            pass

    data_transfers_json = json.dumps(data_transfers, ensure_ascii=False)
    return data_transfers_json