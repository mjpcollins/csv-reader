# csv-reader
CSV Reader relying on no external libraries for an MSc with Bath Uni.

## Install

Make sure to pip install the required libraries before running the code

    pip install -r requirements.txt

## Use
Loading CSVs is done as below

    from utils import read_csv
    
    filename = "tests/data/barometer-1617.csv"
    data = read_csv(filename)

The data is returned as a dict containing lists. Each column is a list in the dict
and accessing a column of data is similar to working with a pandas dataframe. E.g.:

    column_1 = data['DateTime']

A summary of the stats of the file can be obtained with the following code

    from utils import get_stats
    
    filename = "tests/data/barometer-1617.csv"
    stats = get_stats(filename)

This summary is returned as a dict. Here is an example of an output for 
Outside Temperature:

    {'Temperature': {'length': 355,
                     'max': 26.38,
                     'mean': 11.139,
                     'min': -1.81,
                     'standard_deviation': 5.347,
                     'sum': 3954.301,
                     'variance': 28.596},
     'Temperature_range (high)': {'length': 355,
                                  'max': 38.5,
                                  'mean': 15.524,
                                  'min': 1.5,
                                  'standard_deviation': 7.025,
                                  'sum': 5511.1,
                                  'variance': 49.344},
     'Temperature_range (low)': {'length': 355,
                                 'max': 18.7,
                                 'mean': 7.866,
                                 'min': -4.1,
                                 'standard_deviation': 4.872,
                                 'sum': 2792.3,
                                 'variance': 23.737}}

