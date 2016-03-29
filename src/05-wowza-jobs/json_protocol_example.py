__author__ = 'alexcomu'
from mrjob.job import MRJob
import json

class JSONProtocol(object):

    def read(self, line):
        k_str, v_str = line.split('\t', 1)
        return json.loads(k_str), json.loads(v_str)

    def write(self, key, value):
        user_A = str(key[0])
        user_B = str(key[1])
        strinteractionsAll = ";".join(map(str, value))

        #return '%s\t%s' % (json.dumps(key), json.dumps(value))
        return '%s;%s;%s' % (user_A, user_B, strinteractionsAll)


class MRJsonExample(MRJob):

    OUTPUT_PROTOCOL = JSONProtocol

    def mapper(self, key, value):
        (userID, movieID, rating, timestamp) = value.split('\t')
        yield rating, 1

    def reducer(self, rating, occurrences):
        yield rating, sum(occurrences)


if __name__ == '__main__':
    MRJsonExample.run()
