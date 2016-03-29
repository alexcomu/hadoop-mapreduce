__author__ = 'alexcomu'
from mrjob.emr import EMRJobRunner
# check permission on S3 INPUT
EMRJobRunner._check_input_exists = lambda *args: True

from mrjob.job import MRJob
from mrjob.protocol import JSONValueProtocol


class MRTweetWordCount(MRJob):
    INPUT_PROTOCOL = JSONValueProtocol

    def mapper(self, __, tweet):
        text = tweet.get('text', '')
        for word in text.split():
            yield word, 1

    def reducer(self, key, counts):
        yield key, sum(counts)

