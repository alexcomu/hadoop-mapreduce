__author__ = 'alexcomu'
from mrjob.job import MRJob

# Rating Counter

class MRRatingCounter(MRJob):

    def mapper(self, key, value):
        (userID, movieID, rating, timestamp) = value.split('\t')
        yield rating, 1

    def reducer(self, rating, occurrences):
        yield rating, sum(occurrences)


if __name__ == '__main__':
    MRRatingCounter.run()
