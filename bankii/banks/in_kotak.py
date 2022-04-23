import datetime
import typing

from bankii.base.bank import BaseBank
from bankii.utils.util import to_float


class InKotalBank(BaseBank):
    '''
    Statement format for kotak mahindra bank
    0 - Serial
    1 - Transaction date
    2 - Value date
    3 - Description
    4 - Chq / Ref No.
    5 - Debit amount
    6 - Credit amount
    7 - Balance
    8 - Dr/Cr
    '''
    report_file_ext = 'csv'
    country = 'IN'
    name = 'Kotak Bank'
    swift = 'KKBKINBB'
    description = 'Kotak Bank'

    @classmethod
    def is_statement_row(cls, row: typing.List) -> bool:
        try:
            serial_no = int(str(row[0]))
            trans_date = cls.get_statement_date(row)
            balance = cls.get_balance_amount(row)
            return True
        except (ValueError, IndexError):
            return False

    @classmethod
    def get_statement_date(cls, row: typing.List) -> datetime.datetime:
        return datetime.datetime.strptime(row[1],  "%d-%m-%Y")

    @classmethod
    def get_debit_amount(cls, row: typing.List) -> float:
        try:
            amount = to_float(row[5])
            if row[7] == 'DR':
                return amount
            raise ValueError
        except ValueError:
            return float(0.)

    @classmethod
    def get_credit_amount(cls, row: typing.List) -> float:
        try:
            amount = to_float(row[6])
            if row[7] == 'CR':
                return amount
            raise ValueError
        except ValueError:
            return float(0.)

    @classmethod
    def get_balance_amount(cls, row: typing.List) -> float:
        return to_float(row[7])

    @classmethod
    def is_interest_statement(cls, row: typing.List) -> bool:
        if 'Int.Pd:' in str(row[3]):
            return True
        return False

    @classmethod
    def get_statement_reference(cls, row: typing.List) -> str:
        return ', '.join([str(row[3]).strip('="'),str(row[4])])
