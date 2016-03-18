__author__ = 'alexcomu'
from mrjob.job import MRJob

# Word frequency from book
# Dummy Version
# File: 04_book.txt

class MRWordFrequency(MRJob):

    def mapper(self, _, line):
        words = line.split()
        for w in words:
            yield w.lower(), 1

    def reducer(self, word, occurences):
        yield word, sum(occurences)


if __name__ == '__main__':
    MRWordFrequency.run()