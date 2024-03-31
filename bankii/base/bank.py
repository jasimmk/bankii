import datetime
import typing


class BaseBank:
    report_file_pattern = r'^(?P<swift_code>[A-Z]{8})__(?P<currency>[a-zA-Z0-9]{3})__(?P<account_no>[a-zA-Z0-9\-]+)__(?P<file_id>[a-zA-Z0-9\-\_]+).(?P<ext>\w+)$'
    report_file_ext = 'csv'
    country = 'IN'
    name = 'BaseBank'
    swift = '00000000'
    description = 'Base Bank class'
    parser_options = None

    @classmethod
    def is_statement_row(cls, row: typing.List) -> bool:
        pass

    @classmethod
    def get_statement_date(cls, row: typing.List) -> datetime.datetime:
        pass

    @classmethod
    def get_debit_amount(cls, row: typing.List) -> float:
        pass

    @classmethod
    def get_credit_amount(cls, row: typing.List) -> float:
        pass

    @classmethod
    def get_balance_amount(cls, row: typing.List) -> float:
        pass

    @classmethod
    def is_interest_statement(cls, row: typing.List) -> float:
        pass

    @classmethod
    def get_statement_reference(cls, row: typing.List) -> str:
        pass
