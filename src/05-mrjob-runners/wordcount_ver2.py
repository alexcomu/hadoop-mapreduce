__author__ = 'alexcomu'
from mrjob.job import MRJob
from mrjob.protocol import JSONValueProtocol, JSONProtocol


class MRWordFrequencyVer2(MRJob):
    INPUT_PROTOCOL = JSONValueProtocol  # Tell MrJob that each VALUE will be encoded as JSON and we have no KEY.

    def mapper(self, _, line):
        # use regex instead simple split
        for w in line:
            yield w.lower(), 1

    def reducer(self, word, occurrences):
        yield word, sum(occurrences)



class MRWordCounter(MRJob):
    INPUT_PROTOCOL = JSONProtocol  # Key + Value

    def mapper(self, linenum, words):
        # use regex instead simple split
        for w in words:
            yield linenum, 1

    def reducer(self, linenum, occurrences):
        yield linenum, sum(occurrences)
