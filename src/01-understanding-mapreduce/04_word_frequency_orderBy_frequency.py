__author__ = 'alexcomu'
from mrjob.job import MRJob
from mrjob.step import MRStep
import re

# Word frequency from book sorted by frequency
# File: 04_book.txt

# Added new MapReduce job after first reducer

# regular expression used to identify word
WORD_REGEXP = re.compile(r"[\w']+")

class MRWordFrequencyCount(MRJob):

    def steps(self):
        # 2 steps
        return [
            MRStep(mapper=self.mapper_get_words,
                   reducer=self.reducer_count_words),
            MRStep(mapper=self.mapper_make_counts_key,
                   reducer=self.reducer_output_words)
        ]

    # Step 1
    def mapper_get_words(self, _, line):
        words = WORD_REGEXP.findall(line)
        for w in words:
            yield w.lower(), 1

    def reducer_count_words(self, word, values):
        yield word, sum(values)

    # Step 2
    def mapper_make_counts_key(self, word, count):
        # sort by values
        yield '%04d' % int(count), word

    def reducer_output_words(self, count, words):
        # First Column is the count
        # Second Column is the word
        for word in words:
            yield count, word


if __name__ == '__main__':
    MRWordFrequencyCount.run()
