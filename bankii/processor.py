import logging
import re
import typing
from pathlib import Path

import bankii.banks
from bankii.base.bank import BaseBank
from bankii.base.manager import BaseManager
from bankii.base.output import Statement
from bankii.base.reader import BaseRowReader
from bankii.base.writer import BaseWriter

logger = logging.getLogger('bankii')


class ReaderManager(BaseManager):
    readers_class_data: typing.ClassVar[typing.Dict[str, typing.Type[BaseRowReader]]] = None
    readers: typing.ClassVar[typing.Dict[str, BaseRowReader]] = {}

    def initialize(self):
        self.readers_class_data = {}
        subclasses: typing.List[typing.Type[BaseRowReader]] = BaseRowReader.__subclasses__()
        for s in subclasses:
            self.add_reader_class(s)

    def finalize(self):
        for k, reader in self.readers.items():
            reader.finalize()

    def add_reader_class(self, reader: typing.Type[BaseRowReader]):
        self.readers_class_data[reader.get_extension()] = reader

    def get_reader_class(self, reader_type: str) -> typing.Type[BaseRowReader]:
        return self.readers_class_data[reader_type]

    def add_reader(self, file_path: Path, ext: str, parser_options: typing.Dict = None):
        cls = self.get_reader_class(ext)
        reader = cls(file_path, parser_options)
        reader.initialize()
        reader.set_cursor_start()
        self.readers[str(file_path.absolute())] = reader
        return reader

    def get_files_list(self, source_folder: str):
        exts = [ext for ext in self.readers_class_data.keys()]
        files = []
        for ext in exts:
            ext_w = '*.{}'.format(ext)
            files.extend(Path(source_folder).glob(ext_w))
        return files


class WriterManager(BaseManager):
    writers_class_data = None

    def initialize(self):
        self.writers_class_data = {}
        subclasses: typing.List[typing.Type[BaseWriter]] = BaseWriter.__subclasses__()
        for s in subclasses:
            self.add_writer(s)

    def finalize(self):
        pass

    def add_writer(self, writer: typing.Type[BaseWriter]):
        self.writers_class_data[writer.extension] = writer

    def get_writer(self, writer_type: str) -> typing.Type[BaseWriter]:
        return self.writers_class_data[writer_type]


class BankManager(BaseManager):
    banks_map = None
    report_pattern_map = None

    def initialize(self):
        self.banks_map = {}
        self.report_pattern_map = {}
        bankii.banks.initialize()
        subclasses: typing.List[typing.Type[BaseBank]] = BaseBank.__subclasses__()
        for s in subclasses:
            self.add_bank(s)

    def finalize(self):
        pass

    def add_bank(self, bank: typing.Type[BaseBank]):
        self.banks_map[bank.swift] = bank
        if not self.report_pattern_map.get(bank.report_file_pattern):
            self.report_pattern_map[bank.report_file_pattern] = set()
        self.report_pattern_map[bank.report_file_pattern].add(bank)

    def get_bank(self, swift_code: str, file_ext: str) -> typing.Type[BaseBank]:
        bank = self.banks_map[swift_code]
        if bank.report_file_ext == file_ext:
            return bank

    def get_matching_report_names(self, file_names: typing.List[Path]) -> typing.List[
        typing.Tuple[Path, typing.Dict, typing.Type[BaseBank]]]:
        output = []
        invalid_files = set()
        for report_pattern in self.report_pattern_map.keys():
            for file_name_path in file_names:
                file_name = file_name_path.name
                invalid_files.add(str(file_name_path))
                match = re.match(report_pattern, file_name)
                if match and match.groupdict():
                    swift_code = match.groupdict().get('swift_code')
                    ext = match.groupdict().get('ext')
                    bank = self.get_bank(swift_code, ext)
                    report = (file_name_path, match.groupdict(), bank)
                    invalid_files.remove(str(file_name_path))
                    output.append(report)
        str_invalid_files = '\n'.join(invalid_files)
        logger.warning('Skipping below files: \n{}'.format(str_invalid_files))
        return output


class Processor:
    bm: BankManager = None
    rm: ReaderManager = None
    wm: WriterManager = None
    managers = None

    def __init__(self):
        self.bm = BankManager()
        self.rm = ReaderManager()
        self.wm = WriterManager()

        self.managers = [self.bm, self.rm, self.wm]

    def finalize(self):
        for m in self.managers:
            m.finalize()

    def initialize(self):
        for m in self.managers:
            m.initialize()

    # TODO: Make sure output formats are properly organized
    def process(self, source_folder: str, destination_folder: str, output_format: str, output_file: str):
        logger.info('Started processing')
        # Get all files
        files = self.rm.get_files_list(source_folder)
        file_bank_data = self.bm.get_matching_report_names(files)

        # Extract data
        statment: Statement = Statement()

        for bank_report_itr in file_bank_data:
            file_path = bank_report_itr[0]
            report_data = bank_report_itr[1]
            ext = report_data.get('ext')
            bank_class: typing.Type[BaseBank] = bank_report_itr[2]
            parser_options = bank_class.parser_options
            reader = self.rm.add_reader(file_path, ext, parser_options)

            # Read rows
            account_no = report_data.get('account_no')
            swift_code = report_data.get('swift_code')
            currency = report_data.get('currency')
            file_id = report_data.get('file_id')
            while not reader.is_eof():
                line = reader.get_next_row()
                if bank_class.is_statement_row(line):
                    credit_amount = bank_class.get_credit_amount(line)
                    debit_amount = bank_class.get_debit_amount(line)
                    balance_amount = bank_class.get_balance_amount(line)
                    statement_date = bank_class.get_statement_date(line)
                    interest = bank_class.is_interest_statement(line)
                    statement_reference = bank_class.get_statement_reference(line)
                    statment.add_statement_line(**{
                        'account_no': account_no, 'swift_code': swift_code, 'currency': currency, 'interest': interest,
                        'statement_date': statement_date, 'credit_amount': credit_amount,
                        'debit_amount': debit_amount, 'balance_amount': balance_amount,
                        'statement_reference': statement_reference, 'file_id': file_id
                    })
        statment.sort_statements()
        #logger.debug('Output: \n: {}'.format('\n'.join([str(x) for x in statment.to_csv()])))
        # Output data
        # TODO: Better manage the output; CReate folders first
        if not output_file.endswith(output_format):
            output_file = '{}.{}'.format(output_file, output_format)
        if output_format.lower() == 'csv':
            writer = self.wm.get_writer(output_format.lower())
            writer_inst = writer(destination_folder, output_file)
            writer_inst.write_file(statment.to_csv())
        logger.info('Finished processing')