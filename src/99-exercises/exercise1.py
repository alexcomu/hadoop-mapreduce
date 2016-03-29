__author__ = 'alexcomu'
from mrjob.job import MRJob
from mrjob.step import MRStep

# Write a MapReduce job that report the most frequent word grouped by word length.

class MRMostFrequentByLength(MRJob):

    def steps(self):
        return [
            MRStep(mapper=self.mapper_word_occurrences, reducer=self.reducer_by_word_occurrences),
            MRStep(mapper=self.mapper_word_length, reducer=self.reducer_word_length),
            MRStep(mapper=self.order_by_length),
        ]

    def mapper_word_occurrences(self, _, line):
        for phrase in line.split('.'):
            for word in phrase.split():
                if len(word.strip()) > 1:  # Only get words longer than 2 characters, this removes articles and conjunctions
                    yield word.lower(), 1

    def reducer_by_word_occurrences(self, word, occurrences):
        yield word, sum(occurrences)

    def mapper_word_length(self, word, occurrences):
        yield len(word), (occurrences, word)

    def reducer_word_length(self, length_w, occurrencesWord):
        yield length_w, max(occurrencesWord)

    def order_by_length(self, length_w, occurrencesWord):
        yield None, (length_w, occurrencesWord)


if __name__ == '__main__':
    MRMostFrequentByLength.run()
