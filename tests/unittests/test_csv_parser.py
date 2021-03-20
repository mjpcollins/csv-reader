import datetime
from unittest import TestCase
from utils.csv_parser import CSVParser


class TestParser(TestCase):

    def setUp(self):
        self.parser = CSVParser("tests/data/barometer-1617.csv")

    def test_init(self):
        self.assertEqual(r""""((?:[^"]|"")*)"|[^,"\n\r]*(?:,|\r?\n|\r|$)""", self.parser.line_regex.pattern)

    def test_basic_line(self):
        line = '\r\n"2016-10-09 00:00:00","5,4",21.93,21,22.8\r\n'
        expected = ['2016-10-09 00:00:00', '5,4', '21.93', '21', '22.8']
        self.assertEqual(expected, self.parser._parse_line(line))

    def test_newline_line(self):
        line = '"2016-10-09 00:00:00","5,\r""bab""\n4",21.93,21,22.8\r\n'
        expected = ['2016-10-09 00:00:00', '5,\r""bab""\n4', '21.93', '21', '22.8']
        self.assertEqual(expected, self.parser._parse_line(line))

    def test_parse_lines(self):
        self.parser.file_lines = ['"DateTime","Baro"', '"2016-10-09 00:00:00","5\r\n4",21.93,21,22.8\r\n','"2016-10-09 00:00:00","5\r\n4",21.93,21,22.8\r\n','"2016-10-09 00:00:00","5\r\n4",21.93,21,22.8\r\n','"2016-10-09 00:00:00","5\r\n4",21.93,21,22.8\r\n']
        expected = [['2016-10-09 00:00:00', '5\r\n4', '21.93', '21', '22.8'], ['2016-10-09 00:00:00', '5\r\n4', '21.93', '21', '22.8'], ['2016-10-09 00:00:00', '5\r\n4', '21.93', '21', '22.8'], ['2016-10-09 00:00:00', '5\r\n4', '21.93', '21', '22.8']]
        self.assertEqual(expected, self.parser._parse_lines())
        self.assertEqual(['DateTime', 'Baro', 'header_3', 'header_4', 'header_5'], self.parser._header)

    def test_identify_data_type(self):
        self.assertEqual(str, self.parser._identify_column_type([]))
        self.assertEqual(float, self.parser._identify_column_type([1021.9, 1019.9, 1015.8]))
        self.assertEqual(float, self.parser._identify_column_type([1021, 1019.9, 1015]))
        self.assertEqual(float, self.parser._identify_column_type(["1021", "1019.9", "1015"]))
        self.assertEqual(str, self.parser._identify_column_type([1021, "101a9.9", 1015]))
        self.assertEqual(datetime.datetime, self.parser._identify_column_type(["2016-10-09 00:00:00", "2016-10-10 00:00:00", "2016-10-11 00:00:00"]))

    def test_check_datetime(self):
        self.assertEqual(datetime.datetime, self.parser._check_datetime("2016-10-09 00:00:00"))
        self.assertEqual(datetime.datetime, self.parser._check_datetime("00:00:00"))
        self.assertEqual(datetime.datetime, self.parser._check_datetime("2016-10-09"))
        self.assertEqual(str, self.parser._check_datetime("101a9.9"))

    def test_parse_column(self):
        self.assertEqual([1021.0, 1019.9, 1015.0],
                         self.parser._parse_column(["1021", "1019.9", "1015"]))
        self.assertEqual([1021, 1019, 1015],
                         self.parser._parse_column(["1021", "1019", "1015"]))
        self.assertEqual(["1021", "101a9.9", "1015"],
                         self.parser._parse_column([1021, "101a9.9", 1015]))
        self.assertEqual([datetime.datetime(year=2016, month=10, day=9), datetime.datetime(year=2016, month=10, day=10), datetime.datetime(year=2016, month=10, day=11)],
                         self.parser._parse_column(["2016-10-09 00:00:00", "2016-10-10 00:00:00", "2016-10-11 00:00:00"]))
        self.assertEqual([datetime.datetime(year=2016, month=10, day=9), datetime.datetime(year=2016, month=10, day=10), datetime.datetime(year=2016, month=10, day=11)],
                         self.parser._parse_column(["2016-10-09", "2016-10-10", "2016-10-11"]))

    def test_parse_columns(self):
        self.parser._rows = [['2016-10-09 00:00:00', '1021.9'],
                             ['2016-10-10 00:00:00', '1019.9'],
                             ['2016-10-11 00:00:00', '1015.8']]
        self.parser._header = ['DateTime', 'Baro']
        expected_data = {'DateTime': [datetime.datetime(year=2016, month=10, day=9), datetime.datetime(year=2016, month=10, day=10), datetime.datetime(year=2016, month=10, day=11)],
                         'Baro': [1021.9, 1019.9, 1015.8]}
        self.parser._parse_columns()
        self.assertEqual(expected_data, self.parser.data)

    def test_read_csv(self):
        self.parser.file_lines = ['"DateTime","Baro"\n\r',
                                  '"2016-10-09 00:00:00",1021.9\n\r',
                                  '"2016-10-10 00:00:00",1019.9\n\r',
                                  '"2016-10-11 00:00:00",1015.8\n\r']
        expected_data = {'DateTime': [datetime.datetime(year=2016, month=10, day=9), datetime.datetime(year=2016, month=10, day=10), datetime.datetime(year=2016, month=10, day=11)],
                         'Baro': [1021.9, 1019.9, 1015.8]}
        self.assertEqual(expected_data, self.parser.read_csv())
        self.assertEqual(expected_data, self.parser.data)

    def test_can_parse_all_example_data(self):
        indoor_temp = CSVParser('tests/data/indoor-temperature-1617.csv').read_csv()
        outside_temp = CSVParser('tests/data/outside-temperature-1617.csv').read_csv()
        rainfall = CSVParser('tests/data/rainfall-1617.csv').read_csv()
        baro = CSVParser('tests/data/barometer-1617.csv').read_csv()

    def test_bad_data_no_errors(self):
        broken = CSVParser('tests/data/broken-baro.csv').read_csv()
