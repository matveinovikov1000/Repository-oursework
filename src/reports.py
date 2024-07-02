import json
import datetime
import pandas as pd
from src.decorators import decorator
import logging

logger_rep = logging.getLogger(__name__)
file_handler_rep = logging.StreamHandler()
file_formatter_rep = logging.Formatter("%(asctime)s %(filename)s %(levelname)s: %(message)s")
file_handler_rep.setFormatter(file_formatter_rep)
logger_rep.addHandler(file_handler_rep)
logger_rep.setLevel(logging.DEBUG)


def selection_user_date():
    """Функция для запроса даты у пользователя"""
    user_date = input("Введите дату окончания периода выписки в формате ДД.ММ.ГГГГ:\n")
    logger_rep.info("Дата введена")
    return user_date


@decorator
def spending_by_workday(transactions, date):
    """Функция возвращает средние траты за будние и выходные дни"""
    try:
        if date is not None:
            logger_rep.info("Конвертация входной даты из str в datetime")
            select_date = datetime.datetime.strptime(date, "%d.%m.%Y")
    except ValueError:
        logger_rep.warning("В функцию не передана дата. Далее используется текущая дата")
        select_date = datetime.datetime.now()

    transactions_json = transactions.to_json(orient="records", indent=4, force_ascii=False)
    transactions_py = json.loads(transactions_json)
    spendings = []
    period_spendings = []
    spendings_workdays_list = []
    spendings_weekends_list = []
    spendings_workdays_sum = 0
    spendings_weekends_sum = 0

    for spending in transactions_py:
        if spending["Сумма платежа"] < 0:
            logger_rep.info("Выбор операций трат")
            spendings.append(spending)

    for transact in spendings:
        try:
            trans_date = datetime.datetime.strptime(transact["Дата платежа"], "%d.%m.%Y")
            period_trans_date = select_date - datetime.timedelta(hours=2160)
            if period_trans_date <= trans_date <= select_date:
                logger_rep.info("Выбор операций трат за последние 3 месяца")
                period_spendings.append(transact)
        except TypeError:
            logger_rep.warning("Ключ не найден")
            pass

    for transact_period in period_spendings:
        more_trans_date = datetime.datetime.strptime(transact_period["Дата операции"], "%d.%m.%Y %H:%M:%S").weekday()
        if 0 <= more_trans_date <= 4:
            logger_rep.info("Выбор трат в будни + подсчёт общей суммы")
            spendings_workdays_list.append(transact_period)
            spendings_workdays_sum += transact_period["Сумма платежа"]
        elif more_trans_date >= 5:
            logger_rep.info("Выбор трат в выходные + счёт общей суммы")
            spendings_weekends_list.append(transact_period)
            spendings_weekends_sum += transact_period["Сумма платежа"]
    try:
        logger_rep.info("Счёт средних значений трат в будни/выходные")
        spendings_workdays = round(spendings_workdays_sum / len(spendings_workdays_list) * (-1), 2)
        spendings_weekends = round(spendings_weekends_sum / len(spendings_weekends_list) * (-1), 2)

        spendings_week = pd.DataFrame(
            {"Средние траты в будние дни": [spendings_workdays], "Средние траты в выходные дни": [spendings_weekends]})
        return spendings_week
    except ZeroDivisionError:
        logger_rep.warning("При счёте средних знанчений трат выполнено деление на 0, следовательно в выбранном периоде операции не найдены")
        return "В указанный период операции не найдены"
