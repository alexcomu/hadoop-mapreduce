__author__ = 'alexcomu'
from mrjob.job import MRJob

# Minimum Temperature By Location on year 1800
# File: 03_temperature.csv

class MRMinTemperature(MRJob):

    def mapper(self, key, value):
        (location, year, min_or_max, temperature, x, y, z, w) = value.split(',')
        if min_or_max == "TMIN":
            yield location, temperature

    def reducer(self, location, temperatures):
        yield location, min(temperatures)


if __name__ == '__main__':
    MRMinTemperature.run()
