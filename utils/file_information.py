import math
from utils.csv_parser import CSVParser


class FileInformation:

    def __init__(self, filename):
        self.data = CSVParser(filename).read_csv()

    def describe_data(self):
        descriptions = {}
        for column in self.data:
            if type(self.data[column][0]) in {float, int}:
                descriptions[column] = self._calculate_column_stats(column)
        return descriptions

    def _calculate_column_stats(self, column_name):
        column = self.data[column_name]
        col_sum = sum(column)
        col_min = min(column)
        col_max = max(column)
        col_len = len(column)
        col_mean = round(col_sum / col_len, 12)
        col_variance = sum([(v - col_mean) ** 2 for v in column]) / col_len
        col_std = math.sqrt(col_variance)
        stats = {'sum': round(col_sum, 3),
                 'min': round(col_min, 3),
                 'max': round(col_max, 3),
                 'length': round(col_len, 3),
                 'mean': round(col_mean, 3),
                 'variance': round(col_variance, 3),
                 'standard_deviation': round(col_std, 3)}
        return stats
