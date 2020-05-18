import datetime
import typing

from bankii.base.bank import BaseBank
from bankii.utils.util import to_float

class InSbiBank(BaseBank):
    report_file_ext = 'xls'
    country = 'AE'
    name = 'Emirates Islamic Bank'
    swift = 'MEBLAEAD'
    description = 'Emirates Islamic Bank UAE'

    @classmethod
    def is_statement_row(cls, row: typing.List) -> bool:
        try:
            trans_date = datetime.datetime.strptime(row[0], "%d-%m-%Y")
            balance = to_float(row[7])
            return True
        except (ValueError, IndexError):
            return False

    @classmethod
    def get_statement_date(cls, row: typing.List) -> datetime.datetime:
        return datetime.datetime.strptime(row[0], "%d-%m-%Y")

    @classmethod
    def get_debit_amount(cls, row: typing.List) -> float:
        try:
            return to_float(row[5])
        except ValueError:
            return float(0.)

    @classmethod
    def get_credit_amount(cls, row: typing.List) -> float:
        try:
            return to_float(row[4])
        except ValueError:
            return float(0.)

    @classmethod
    def get_balance_amount(cls, row: typing.List) -> float:
        return to_float(row[7])

    @classmethod
    def is_interest_statement(cls, row: typing.List) -> bool:
        if 'PROFIT POOL PAYOUT/' in str(row[1]):
            return True
        return False

    @classmethod
    def get_statement_reference(cls, row: typing.List) -> str:
        return str(row[1]).strip()
