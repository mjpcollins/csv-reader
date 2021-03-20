import re
import json
import datetime
import dateutil.parser


class CSVParser:

    def __init__(self, file):
        with open(file, 'r') as F:
            self.file_lines = F.readlines()
            self.file_lines[-1] += "\r\n"
        self.line_regex = re.compile(r""""((?:[^"]|"")*)"|[^,"\n\r]*(?:,|\r?\n|\r|$)""")
        self._header = None
        self._rows = None
        self.data = {}

    def read_csv(self):
        self._parse_lines()
        self._parse_columns()
        return self.data

    def _parse_lines(self):
        self._rows = [self._parse_line(line) for line in self.file_lines]
        longest_row = max((len(row) for row in self._rows))
        self._header = [header.replace('"', '') for header in self._rows.pop(0)]
        self._rows = [row + [''] * (longest_row - len(row)) for row in self._rows]  # Padding clean up
        self._header = self._header + [f"header_{idx}" for idx in range(1, longest_row + 1) if idx > len(self._header)]
        return self._rows

    def _parse_line(self, line):
        line_parsed = []
        for idx, item in enumerate(self.line_regex.finditer(line)):
            if (idx == 0) and (item.string[0] == ','):
                line_parsed.append('')
            elif item.groups()[0]:
                line_parsed.append(item.groups()[0])
            else:
                bad_parsing = line[item.start(): item.end()][:-1].strip()
                if bad_parsing:
                    line_parsed.append(bad_parsing)
        return line_parsed

    def _parse_columns(self):
        for col_index in range(len(self._rows[0])):
            column = []
            for row in self._rows:
                try:
                    column.append(row[col_index])
                except IndexError:
                    pass
            self.data[self._header[col_index]] = self._parse_column(column)

    def _parse_column(self, column):
        data_type = self._identify_column_type(column)
        if data_type in {str, float, int}:
            return [data_type(value) for value in column]
        elif data_type == datetime.datetime:
            return [dateutil.parser.parse(value) for value in column]
        else:
            raise TypeError(f'Unsupported value type of {data_type}')

    def _identify_column_type(self, column):
        suspected_type = str
        if column:
            types = set()
            for value in column:
                try:
                    types.add(type(json.loads(f'{value}')))
                except json.JSONDecodeError:
                    suspected_value_type = self._check_datetime(value)
                    types.add(suspected_value_type)
            if str in types:
                return suspected_type
            elif len(types) == 1:
                suspected_type = list(types)[0]
            elif float in types:
                suspected_type = float
            elif int in types:
                suspected_type = int
        return suspected_type

    @staticmethod
    def _check_datetime(suspected_value):
        try:
            return type(dateutil.parser.parse(suspected_value))
        except ValueError:
            return str


def read_csv(filename):
    return CSVParser(filename).read_csv()
