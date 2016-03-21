__author__ = 'alexcomu'
from mrjob.job import MRJob
import re

# Word frequency from book
# Dummy Version
# File: 04_book.txt

# regular expression used to identify word
WORD_REGEXP = re.compile(r"[\w']+")


class MRWordFrequencyDummyClass(MRJob):

    def mapper(self, _, line):
        words = line.split()
        for w in words:
            yield w.lower(), 1

    def reducer(self, word, occurrences):
        yield word, sum(occurrences)


class MRWordFrequencyBetterWay(MRJob):

    def mapper(self, _, line):
        # use regex instead simple split
        words = WORD_REGEXP.findall(line)
        for w in words:
            yield w.lower(), 1

    def reducer(self, word, occurrences):
        yield word, sum(occurrences)


if __name__ == '__main__':
    MRWordFrequencyBetterWay.run()
    #MRWordFrequencyDummyClass.run()