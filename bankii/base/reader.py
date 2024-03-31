import _csv
import csv
import typing
from pathlib import Path

import xlrd


class BaseRowReader:
    _file_path: Path = None
    _file_handler: typing.IO = None
    _file_reader = None
    _extension: str = None
    _row: int = 0
    _eof = False
    _parser_options = None

    def __init__(self, file_path: Path, parser_options: typing.Dict = None):
        if file_path.suffix.lower() == '.{}'.format(self._extension):
            self._file_path = file_path
            self._parser_options = parser_options
        else:
            raise ValueError('Invalid file: {} passed for class: {}'.format(file_path, self.__class__))

    def initialize(self):
        pass

    def finalize(self):
        if self._file_handler:
            self._file_handler.close()

    def get_next_row(self) -> typing.List[typing.Tuple]:
        pass

    def set_cursor_start(self):
        self._row = 0
        self._eof = False

    def is_eof(self) -> bool:
        return self._eof

    @classmethod
    def get_extension(cls):
        return cls._extension


class CSVRowReader(BaseRowReader):
    _extension = 'csv'
    _file_reader: _csv.reader = None
    _row: int = 0
    _parser_options = None

    def initialize(self):
        file_absolute = str(self._file_path.absolute())
        self._file_handler = open(file_absolute, 'r')
        if self._parser_options:
            self._file_reader = csv.reader(self._file_handler, **self._parser_options)
        else:
            self._file_reader = csv.reader(self._file_handler)

    def set_cursor_start(self):
        self._row = 0
        self._file_handler.seek(0)
        self._eof = False

    def get_next_row(self) -> typing.List[typing.Tuple]:
        try:
            line = next(self._file_reader)
            self._row += 1
            return line
        except StopIteration:
            self._eof = True
        return []


class XLSRowReader(BaseRowReader):
    _extension = 'xls'
    _file_reader: xlrd.sheet.Sheet = None
    _row = 0
    _eof = False

    def initialize(self):
        file_absolute = str(self._file_path.absolute())
        xlrd.xlsx.ensure_elementtree_imported(False, None)
        xlrd.xlsx.Element_has_iter = True
        work_book = xlrd.open_workbook(file_absolute)
        # TODO: Any bank give report on second sheet?
        self._file_reader = work_book.sheet_by_index(0)
        self._eof = False

    def get_next_row(self) -> typing.List[typing.Tuple]:
        if self._file_reader and self._row < self._file_reader.nrows:
            row = self._file_reader.row_values(self._row)
            self._row += 1
            return row
        self._eof = True
        return []
