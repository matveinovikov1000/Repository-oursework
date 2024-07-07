from src.read_operations import read_operations_dataframe
from src.reports import spending_by_workday


def test_spending_by_workday():
    assert (
        spending_by_workday(transactions=read_operations_dataframe(filename="operations_test.xls"), date="21.12.2021")
        is None
    )
