# csv-reader
CSV Reader relying on no external libraries for an MSc with Bath Uni.

## Use
Loading CSVs is done as below

    from utils import read_csv
    
    filename = "tests/data/barometer-1617.csv"
    data = read_csv(filename)

A summary of the stats of the file can be obtained with the following code

    from utils import get_stats
    
    filename = "tests/data/barometer-1617.csv"
    stats = get_stats(filename)

