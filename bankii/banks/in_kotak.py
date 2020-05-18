import datetime
import typing

from bankii.base.bank import BaseBank
from bankii.utils.util import to_float


class InKotalBank(BaseBank):
    report_file_ext = 'csv'
    country = 'IN'
    name = 'Kotak Bank'
    swift = 'KKBKINBB'
    description = 'Kotak Bank'

    @classmethod
    def is_statement_row(cls, row: typing.List) -> bool:
        try:
            serial_no = int(str(row[0]))
            trans_date = datetime.datetime.strptime(str(row[1]), "%d/%m/%Y")
            balance = to_float(row[6])
            return True
        except (ValueError, IndexError):
            return False

    @classmethod
    def get_statement_date(cls, row: typing.List) -> datetime.datetime:
        return datetime.datetime.strptime(row[1], "%d/%m/%Y")

    @classmethod
    def get_debit_amount(cls, row: typing.List) -> float:
        try:
            amount = to_float(row[4])
            if row[5] == 'DR':
                return amount
            raise ValueError
        except ValueError:
            return float(0.)

    @classmethod
    def get_credit_amount(cls, row: typing.List) -> float:
        try:
            amount = to_float(row[4])
            if row[5] == 'CR':
                return amount
            raise ValueError
        except ValueError:
            return float(0.)

    @classmethod
    def get_balance_amount(cls, row: typing.List) -> float:
        return to_float(row[6])

    @classmethod
    def is_interest_statement(cls, row: typing.List) -> bool:
        if 'Int.Pd:' in str(row[2]):
            return True
        return False

    @classmethod
    def get_statement_reference(cls, row: typing.List) -> str:
        return str(row[2]).strip('="')
