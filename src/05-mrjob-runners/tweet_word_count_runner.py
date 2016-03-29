__author__ = 'alexcomu'
from tweet_word_count import MRTweetWordCount
import json

# Setup loggings so we se errors in case
import logging
logging.basicConfig(level=logging.INFO)

# How to run on a persistent JOB FLOW
#MRJOB_FLOWID = 'JOB-ID'

# How to take the file as input from S3
#INPUT_FILE = 's3://.....'


# Configure the MR job with the options to run on EMR, load the conf from MRJOB.CONF,
# use the specified JOBFLOW to run map reduce and use the INPUT_FILE as the input source
# mr_job = MRTweetWordCount(args=['-v', '-r', 'emr',
#                                 '--conf-path', 'mrjob.conf',
#                                 INPUT_FILE])

mr_job = MRTweetWordCount()
mr_job.stdin = open('utils/tweet_example.json')

output = {}
with mr_job.make_runner() as runner:
    runner.run()
    for line in runner.stream_output():
        key, value = mr_job.parse_output_line(line)
        if int(value) > 1:  # Only get words that appear more than once.
            output[key] = value

# Print the output in JSON
print json.dumps(output)