from mrjob.job import MRJob
from mrjob.protocol import JSONValueProtocol 


class MRWordFreqJSON(MRJob):
    INPUT_PROTOCOL = JSONValueProtocol  # Tell MrJob that each VALUE will be encoded as JSON and we have no KEY.

    def mapper(self, _, value):
        for word in value:  # As VALUE is a list of words we just iterate over it and emit each word.
            yield word, 1

    def reducer(self, word, counts):
        yield word, sum(counts)


if __name__ == '__main__':
    MRWordFreqJSON.run()
