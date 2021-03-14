import re
import json
import datetime


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
        self._header = [header.replace('"', '') for header in self._rows.pop(0)]
        return self._rows

    def _parse_line(self, line):
        line_parsed = []
        for item in self.line_regex.finditer(line):
            if item.groups()[0]:
                line_parsed.append(item.groups()[0])
            else:
                bad_parsing = line[item.start(): item.end()][:-1].strip()
                if bad_parsing:
                    line_parsed.append(bad_parsing)
        return line_parsed

    def _parse_columns(self):
        for col_index in range(len(self._rows[0])):
            column = [row[col_index] for row in self._rows]
            self.data[self._header[col_index]] = self._parse_column(column)

    def _parse_column(self, column):
        data_type = self._identify_column_type(column)
        if data_type in {str, float, int}:
            return [data_type(value) for value in column]
        elif data_type == datetime.datetime:
            return [datetime.datetime.strptime(value, "%Y-%m-%d %H:%M:%S") for value in column]
        elif data_type == datetime.date:
            return [datetime.datetime.strptime(value, "%Y-%m-%d").date() for value in column]
        elif data_type == datetime.time:
            return [datetime.datetime.strptime(value, "%H:%M:%S").time() for value in column]
        else:
            raise TypeError(f'Unsupported value type of {data_type}')

    def _identify_column_type(self, column):
        suspected_type = None
        if column:
            types = set()
            for value in column:
                try:
                    types.add(type(json.loads(f'{value}')))
                except json.JSONDecodeError:
                    suspected_value_type = self._check_datetime(value)
                    types.add(suspected_value_type)
            if str in types:
                suspected_type = str
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
            return type(datetime.datetime.strptime(suspected_value, "%Y-%m-%d %H:%M:%S"))
        except ValueError as e:
            if str(e) == "day is out of range for month":
                print("How did this happen")

        try:
            return type(datetime.datetime.strptime(suspected_value, "%Y-%m-%d").date())
        except ValueError:
            pass

        try:
            return type(datetime.datetime.strptime(suspected_value, "%H:%M:%S").time())
        except ValueError:
            return str


if __name__ == '__main__':
    indoor_temp = CSVParser('../tests/data/indoor-temperature-1617.csv').read_csv()
    outside_temp = CSVParser('../tests/data/outside-temperature-1617.csv').read_csv()
    rainfall = CSVParser('../tests/data/rainfall-1617.csv').read_csv()
    baro = CSVParser('../tests/data/barometer-1617.csv').read_csv()
    print(baro)
