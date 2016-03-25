__author__ = 'alexcomu'
from mrjob.job import MRJob

class StarWarsSims(MRJob):

    def mapper(self, key, line):
        (movieName, value) = line.split('\t')
        if (movieName == '"Star Wars: Episode IV - A New Hope (1977)"'):
            (bracket, simName, values) = value.split('"')
            (empty, score, coraters) = values.split(',')
            cleanCoraters = coraters.split(']')
            numCoraters = int(cleanCoraters[0])
            if (numCoraters > 500):
                yield float(score), (simName, numCoraters)

    def reducer(self, key, values):
        for value in values:
            yield key, value

if __name__ == '__main__':
    StarWarsSims.run()
