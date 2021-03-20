from utils import get_stats, read_csv
from matplotlib import pyplot as plt
import pprint


good_data = "tests/data/outside-temperature-1617.csv"
error_data = "tests/data/outside-temperature-1617-errors.csv"


def show_all_stats():
    print("\nBarometer Readings:")
    pprint.pprint(get_stats("tests/data/barometer-1617.csv"))
    print("\nIndoor Temperature:")
    pprint.pprint(get_stats("tests/data/indoor-temperature-1617.csv"))
    print("\nOutside Temperature:")
    pprint.pprint(get_stats(good_data))
    print("\nRainfall:")
    pprint.pprint(get_stats("tests/data/rainfall-1617.csv"))


def show_stats_for_altered_file():
    print("\nUnaltered Stats:")
    pprint.pprint(get_stats(good_data))
    print("\nAltered Stats:")
    pprint.pprint(get_stats(error_data))


def draw_chart():
    data_good = read_csv(good_data)
    data_error = read_csv(error_data)
    X = data_good['DateTime']
    plt.plot(X, data_good['Temperature'], color='b', linewidth=1)
    plt.plot(X, data_good['Temperature_range (low)'], color='b', linewidth=1)
    plt.plot(X, data_good['Temperature_range (high)'], color='b', linewidth=1)
    plt.plot(X, data_error['Temperature'], '--', color='grey', linewidth=1)
    plt.plot(X, data_error['Temperature_range (low)'], '--', color='grey', linewidth=1)
    plt.plot(X, data_error['Temperature_range (high)'], '--', color='grey', linewidth=1)
    plt.show()


if __name__ == '__main__':
    show_all_stats()
