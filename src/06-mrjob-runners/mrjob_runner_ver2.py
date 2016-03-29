__author__ = 'alexcomu'
from wordcount_ver2 import MRWordFrequencyVer2, MRWordCounter
from mrjob.protocol import JSONValueProtocol, JSONProtocol



TEXT = [
    ["Lorem", "ipsum", "dolor", "sit", "amet,", "consectetur", "adipiscing", "elit"],
    ["Quisque", "molestie", "lacus", "a", "iaculis", "tempus"],
    ["Nam", "lorem", "nulla,", "viverra", "non", "pulvinar", "ut,", "fermentum", "et", "tortor"],
    ["Cras", "vitae", "libero", "sed", "purus", "venenatis", "posuere"],
    ["Proin", "commodo", "risus", "augue", "vitae", "suscipit", "lectus", "accumsan", "sit", "amet"],
    ["Praesent", "eu", "erat", "sem"],
    ["Pellentesque", "interdum", "porta", "libero", "et", "ultrices", "nunc", "eleifend", "sit", "amet"],
    ["In", "in", "mauris", "nec", "elit", "ullamcorper", "ultrices", "at", "ac", "ante"],
    ["Suspendisse", "potenti"],
    ["Aenean", "eu", "nisl", "in", "ante", "adipiscing", "imperdiet"],
    ["Ut", "pulvinar", "lectus", "quis", "feugiat", "adipiscing"],
    ["Nunc", "vulputate", "mauris", "congue", "diam", "ultrices", "aliquet"],
    ["Nulla", "pharetra", "laoreet", "est", "quis", "vestibulum"],
    ["Quisque", "feugiat", "pharetra", "sagittis"],
    ["Phasellus", "nulla", "massa", "sodales", "a", "suscipit", "blandit", "facilisis", "eu", "augue"],
    ["Cras", "mi", "massa", "ullamcorper", "nec", "tristique", "at", "convallis", "quis", "eros"],
    ["Mauris", "non", "fermentum", "lacus", "vitae", "tristique", "tellus"],
    ["In", "volutpat", "metus", "augue", "nec", "laoreet", "ante", "hendrerit", "vitae"],
    ["Vivamus", "id", "lacus", "nec", "orci", "tristique", "vulputate"]
]


mr_job = MRWordCounter()
#mr_job.stdin = [JSONValueProtocol().write(None, line) for line in TEXT]        ## JSONValueProtocol doesn't need a key
mr_job.stdin = [JSONProtocol().write(linenum, line) for linenum, line in enumerate(TEXT)]

with mr_job.make_runner() as runner:
        runner.run()
        for line in runner.stream_output():
            key, value = mr_job.parse_output_line(line)
            print "Line: ", key, " Count: ", value