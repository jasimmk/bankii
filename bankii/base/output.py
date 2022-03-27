import datetime
import operator
import typing
from collections import OrderedDict

from bankii.utils.util import to_date, to_float


class StatementLine:
    account_no: str = None
    swift_code: str = None
    currency: str = None
    file_id: str = None
    credit_amount: float = None
    debit_amount: float = None
    balance_amount: float = None
    statement_date: datetime.datetime = None
    interest: bool = None
    statement_reference: str = None

    def __init__(self, **statement_line_args):
        for k, v in statement_line_args.items():
            setattr(self, k, v)


class Statement:
    statements: typing.List[StatementLine] = None
    output_format = OrderedDict({
        'account_no': {
            'title': 'Account Number',
            'format': str
        },
        'swift_code': {
            'title': 'Swift',
            'format': str
        },
        'currency': {
            'title': 'Currency',
            'format': str},
        'statement_date': {
            'title': 'Date',
            'format': to_date
        },
        'statement_reference': {
            'title': 'Satement Reference',
            'format': str
        },
        'credit_amount': {
            'title': 'Credit',
            'format': to_float
        },
        'debit_amount': {
            'title': 'Debit',
            'format': to_float
        },
        'balance_amount': {
            'title': 'Balance',
            'format': to_float
        },
        'interest': {
            'title': 'Interest',
            'format': str
        },
        'file_id': {
            'title': 'File ID',
            'format': str
        }
    })

    def __init__(self):
        self.statements = []

    def len(self):
        return len(self.statements)

    def is_empty(self):
        return len(self.statements) == 0

    def add_statement_line(self, **statement_line_args):
        statement_line = StatementLine(**statement_line_args)
        self.statements.append(statement_line)

    def get_statement_header(self):
        return [x.get('title') for x in self.output_format.values()]

    def sort_statements(self, column: str = 'statement_date', order: int = 1):
        options = {
            'key': operator.attrgetter(column)
        }
        if order == -1:
            options['reverse'] = True
        self.statements = sorted(self.statements, **options)

    def to_csv(self) -> typing.List:
        output = list()
        output.append(self.get_statement_header())
        output_order = [k for k in self.output_format.keys()]
        for statement_line in self.statements:
            line = []
            for k in output_order:
                data = getattr(statement_line, k, '')
                format_fn = self.output_format.get(k, {}).get('format')
                if format_fn:
                    data = format_fn(data)
                line.append(data)
            output.append(line)
        return output
