import csv
import typing
from pathlib import Path


class BaseWriter:
    file_name = None
    destination_dir = None
    extension = None

    def __init__(self, destination_dir, file_name):
        self.destination_dir = destination_dir
        self.file_name = file_name

    def write_file(self, data):
        path = Path(self.destination_dir)
        path.mkdir(parents=True, exist_ok=True)
        file_path = path / self.file_name
        with file_path.open('w', encoding='utf-8') as f:
            f.write(data)


class CSVWriter(BaseWriter):
    extension = 'csv'
    options = {
        'delimiter': ',',
        'quotechar': '"',
        'quoting': csv.QUOTE_MINIMAL
    }

    def write_file(self, data: typing.List[typing.List]):
        path = Path(self.destination_dir)
        path.mkdir(parents=True, exist_ok=True)
        file_path = path / self.file_name
        with file_path.open('w', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile, **self.options)
            for line in data:
                csv_writer.writerow(line)
