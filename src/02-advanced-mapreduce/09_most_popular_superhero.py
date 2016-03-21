__author__ = 'alexcomu'
from mrjob.job import MRJob
from mrjob.step import MRStep

# Count # of friends per character, per line
# Aggregate per character
# Mapper to evaluate the maximum value (using tuple)
# Find the max value

class MRMostPopularSuperHero(MRJob):

    def configure_options(self):
        super(MRMostPopularSuperHero, self).configure_options()
        self.add_file_option('--names', help='Path to SuperHero names')

    def steps(self):
        return [
            MRStep(mapper=self.mapper_superhero_friends,
                   reducer_init=self.reducer_init,
                   reducer=self.reduce_superhero_friends),
            MRStep(reducer=self.reduce_output)
        ]

    #step 1
    def mapper_superhero_friends(self, _, line):
        splitted = line.split(" ")
        yield splitted[0], len(splitted)-1

    def reducer_init(self):
        self.superhero_names = {}
        with open('09_Marvel-Names.txt') as f:
            for line in f:
                fields = line.split('"')
                self.superhero_names[fields[0]] = " ".join(fields[1:])
            # Alternartive
            # for line in f:
            #     fields = line.split(" ")
            #     self.superhero_names[fields[0]] = unicode(fields[1], errors='ignore')

    def reduce_superhero_friends(self, superhero, friends_len):
        yield None, (sum(friends_len), self.superhero_names[superhero])

    #step 2
    def reduce_output(self, key, values):
        yield max(values)


if __name__ == '__main__':
    MRMostPopularSuperHero.run()