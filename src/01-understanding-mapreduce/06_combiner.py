__author__ = 'alexcomu'
from mrjob.job import MRJob

# Word frequency from book using combiner
# File: 04_book.txt

class MRWordFrequencyCount(MRJob):

    def mapper(self, _, line):
        words = line.split()
        for w in words:
            yield w.lower(), 1

    def combiner(self, word, occurrences):
        # same input as reducer -> useful on elastic map reduce to do some reduction for improvements
        yield word, sum(occurrences)

    def reducer(self, word, occurrences):
        yield word, sum(occurrences)

if __name__ == '__main__':
    MRWordFrequencyCount.run()
