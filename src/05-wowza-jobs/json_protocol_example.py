__author__ = 'alexcomu'
from mrjob.job import MRJob
from mrjob.protocol import JSONProtocol, RawValueProtocol


class MRJsonExample(MRJob):

    OUTPUT_PROTOCOL = RawValueProtocol
    pass


if __name__ == '__main__':
    MRJsonExample.run()
