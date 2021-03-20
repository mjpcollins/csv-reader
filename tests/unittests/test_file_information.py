from unittest import TestCase
from utils.file_information import FileInformation


class TestParser(TestCase):

    def setUp(self):
        self.indoor_temp = FileInformation('tests/data/indoor-temperature-1617.csv')
        self.outside_temp = FileInformation('tests/data/outside-temperature-1617.csv')
        self.rainfall = FileInformation('tests/data/rainfall-1617.csv')
        self.baro = FileInformation('tests/data/barometer-1617.csv')

    def test_calculate_column_stats_baro(self):
        expected_stats = {'sum': 358549.6,
                          'min': 979.6,
                          'max': 1035.6,
                          'length': 355,
                          'mean': 1009.999,
                          'variance': 97.136,
                          'standard_deviation': 9.856}
        actual_stats = self.baro._calculate_column_stats('Baro')
        self.assertEqual(expected_stats, actual_stats)

    def test_calculate_column_stats_humidity(self):
        expected_stats = {'sum': 17176,
                          'min': 37,
                          'max': 59,
                          'length': 354,
                          'mean': 48.520,
                          'variance': 26.848,
                          'standard_deviation': 5.182}
        actual_stats = self.indoor_temp._calculate_column_stats('Humidity')
        self.assertEqual(expected_stats, actual_stats)

    def test_descriptions(self):
        expected_stats = {'Baro': {'sum': 358549.6,
                                   'min': 979.6,
                                   'max': 1035.6,
                                   'length': 355,
                                   'mean': 1009.999,
                                   'variance': 97.136,
                                   'standard_deviation': 9.856}}
        actual_stats = self.baro.describe_data()
        self.assertEqual(expected_stats, actual_stats)
