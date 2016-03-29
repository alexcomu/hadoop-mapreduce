__author__ = 'alexcomu'
from wordcount import MRWordFrequency

mr_job = MRWordFrequency()
mr_job.stdin = open('utils/04_book.txt')

with mr_job.make_runner() as runner:
        runner.run()
        for line in runner.stream_output():
            key, value = mr_job.parse_output_line(line)
            print "Word: ", key, " Count: ", value