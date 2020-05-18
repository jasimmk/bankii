import datetime
import typing

from bankii.base.bank import BaseBank
from bankii.utils.util import to_float


class InSbiBank(BaseBank):
    report_file_ext = 'csv'
    country = 'IN'
    name = 'SBI Bank'
    swift = 'SBININBB'
    description = 'State Bank of India'
    parser_options = {
        'delimiter': '\t'
    }

    @classmethod
    def is_statement_row(cls, row: typing.List) -> bool:
        try:
            trans_date = datetime.datetime.strptime(row[1], "%d %b %Y")
            balance = to_float(row[6])
            return True
        except (ValueError, IndexError):
            return False

    @classmethod
    def get_statement_date(cls, row: typing.List) -> datetime.datetime:
        return datetime.datetime.strptime(row[1], "%d %b %Y")

    @classmethod
    def get_debit_amount(cls, row: typing.List) -> float:
        try:
            return to_float(row[4])
        except ValueError:
            return float(0.)

    @classmethod
    def get_credit_amount(cls, row: typing.List) -> float:
        try:
            return to_float(row[5])
        except ValueError:
            return float(0.)

    @classmethod
    def get_balance_amount(cls, row: typing.List) -> float:
        return to_float(row[6])

    @classmethod
    def is_interest_statement(cls, row: typing.List) -> bool:
        if 'CREDIT INTEREST---' in row[2]:
            return True
        return False

    @classmethod
    def get_statement_reference(cls, row: typing.List) -> str:
        return row[2].strip()
