import datetime
import typing

from bankii.base.bank import BaseBank
from bankii.utils.util import to_float


class InFederalBank(BaseBank):
    report_file_ext = 'xls'
    country = 'IN'
    name = 'Federal Bank'
    swift = 'FDRLINBB'
    description = 'Federal Bank class'

    @classmethod
    def is_statement_row(cls, row: typing.List) -> bool:
        try:
            serial_no = int(row[0])
            trans_date = datetime.datetime.strptime(row[1], "%d/%m/%Y")
            balance = to_float(row[9])
            return True
        except (ValueError, IndexError):
            return False

    @classmethod
    def get_statement_date(cls, row: typing.List) -> datetime.datetime:
        return datetime.datetime.strptime(row[1], "%d/%m/%Y")

    @classmethod
    def get_debit_amount(cls, row: typing.List) -> float:
        try:
            return to_float(row[7])
        except ValueError:
            return float(0.)

    @classmethod
    def get_credit_amount(cls, row: typing.List) -> float:
        try:
            return to_float(row[8])
        except ValueError:
            return float(0.)

    @classmethod
    def get_balance_amount(cls, row: typing.List) -> float:
        return to_float(row[9])

    @classmethod
    def is_interest_statement(cls, row: typing.List) -> bool:
        if 'SBINT:' in row[2]:
            return True
        return False

    @classmethod
    def get_statement_reference(cls, row: typing.List) -> str:
        return row[2]
