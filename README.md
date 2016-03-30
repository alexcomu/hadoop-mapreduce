# Map Reduce

## Requirements

We need:

	- Python 2.7
	- Virtualenv (pip install virtualenv && virtuale envMyEnv && source envMyEnv/bin/activate) 
	- MrJob (pip install mrjob)
	- Download MovieData DB (100K) http://grouplens.org/datasets/movielens/ 
	- Put the unzip folder into src-movies folder


Check -> https://github.com/alexcomu/big-data-basics to read a simple introduction on MapReduce and Hadoop.


## Basic MapReduce - Example 

Check the example under the folder: src/01-understanding-mapreduce/...

### 01_rating_counter.py

Count occurrences of rating value from movie DB.

### 02_avarage_friends.py

Calculate For each Age the Avarage of friends. Data (csv) Structure:

	ID, Name, Age, Number of Friends

How to Run:

	$ python src/01-understanding-mapreduce/02_avarage_friends.py CSV-SOURCE.csv > result.txt


### 03_temperature_extreme.py

Check for each location the minimum or maximum temperature.

Src file:

     03_temperature.csv

How to Run:

     $ python src/01-understanding-mapreduce/03_temperature_extreme.py CSV-SOURCE.csv > result.txt
     
     
### 04_word_frequency.py

Calculate the word frequency from a book source.

How to Run:

     $ python src/01-understanding-mapreduce/04_word_frequency.py CSV-SOURCE.csv > result.txt

### 04_word_frequency_orderBy_frequency.py

Calculate word frequency and then order the list by frequency using 2 MapReduce Jobs in series.

The Input of the second job will be the output of the first one, so the second Map function will sort the result of the first reducer by occurrences and the second Reducer will only print the result.

How to Run:

     $ python src/01-understanding-mapreduce/04_word_frequency_orderBy_frequency.py CSV-SOURCE.csv > result.txt

### 05_total_spend_by_customer.py

For each customer from an input file (05_customer_order.csv) extract how much he spent.

How to Run:

     $ python src/01-understanding-mapreduce/05_total_spend_by_customer.py CSV-SOURCE.csv > result.txt
     
### Combiners

Is like embedding reducer part into mapping function to have more efficient processes. 
Check the example "06_combiner_example1.py"! Is quite useful on elastic map reduce to do some reduction for improvements

## Advanced MapReduce - Example

### 07_most_rated_movie

Count occurrences of each movie rating from movie DB and find the most rated movie.

### 08_quick_lookup

Add to the previous example the name of the movie, readed from u.item file using **configure_options** and **reducer_init**!

How to Run:

     $ python src/02-advanced-mapreduce/08_quick_lookup.py --items=PATH-TO-u.ITEM PATH-TO-u.DATA > result.txt

## Superhero Social Network

### Most Popular Superhero

We want find the most popular superhero from a source data like this:

    SuperHeroID1 Friend1 Friend2 ...
    SuperHeroID2 Friend1 Friend2 ...
    SuperHeroID1 Friend1 Friend2 ...

Process:

- Count # of friends per character, per line
- Aggregate per character
- Mapper to evaluate the maximum value (using tuple)
- Find the max value

There are 2 examples **09_most_popular_superhero.py**, check it out!

How to run:

    $ python src/02-advanced-mapreduce/09_most_popular_superhero.py utils/09_Marvel-Graph.txt --names=utils/09_Marvel-Names.txt
    
    
## Degrees of Separation: Breadth-First Search

Degree of separation between heroes! BFS: Breadth-First Search -> imagine to have a graph of characters, where circle = character and arc = connection. What is the distance between of 2 characters? Check the examples!

Source: https://en.wikipedia.org/wiki/Breadth-first_search

We’ll use the Marvel DB file, following this steps:

### Represent each line as a BFS Node, with color and distance

From:
     $ HeroID Friend1 Friend2

To:
     $ HeroID | Friends List | Distance | Color

Assuming distance: 9999 -> Infinite and color: WHITE / BLACK except for the starting node (we’re calculating the degree of separation from the first Hero). Is a continuos process of several iterations: INTPU -> OUTPUT -> INPUT -> OUTPUT -> … Using file write / read at each iterations.

We’ll use a counter  to indicate how many times we hit the single character we’re looking for. Any mapper and any reducer can increment the counter, this is very important.

Steps:

     - Create a new file with the correct BFS format (10_process_Marvel.py) starting from an HeroID
     - python src/03-degrees-of-separation/10_process_Marvel.py HEROID
     - Use MapReduce to extract what we are looking for!
     - python src/03-degrees-of-separation/11_degrees_separation.py --target=100 src/03-degrees-of-separation/BFS-iteration-0.txt > src/03-degrees-of-separation/BFS-iteration-1.txt
     - python src/03-degrees-of-separation/11_degrees_separation.py --target=100 src/03-degrees-of-separation/BFS-iteration-1.txt > src/03-degrees-of-separation/BFS-iteration-2.txt
     - python src/03-degrees-of-separation/11_degrees_separation.py --target=100 src/03-degrees-of-separation/BFS-iteration-2.txt > src/03-degrees-of-separation/BFS-iteration-3.txt
     - ....
     - Until we received the result!
     
## Find Similar Movies Based on Rating with MapReduce

### Movie recommendation

We'll use the MovieLands Dataset following this steps:
 
    - Find every pair of movies that were watched by tha same person
    - Measure the similarity of their rating across all users who watched both
    - Sort by movie, then by similarity strength

### MapReduce Problem

Map reduce problem, 2 steps:

    Mapper: Extract User -> (Movie, Rating)
    Reducer: Groups all movie, rating pairs by user

    Mapper: Output all movies viewed by the same user (movie1, movie2) -> (rating1, rating2)
    Reducer: Compute rating-based similarity between each movie pair (movie1, movie2) -> (similarity, number of users who saw both)

    Mapper: Make movie name, similarity score the sorting key
    Reducer: Display the final sorted output
    
    Output: -> Movie sorted by Name with a list of movie ordered by similaity
    Format:  "MOVIE_NAME" ["SIMILAR_MOVIE", "SIMILAR_POINT (From 0 to 1)", "Number of people who votes both"]
    Example: "Start Wars 1977" ["Empire Strikes Back 1980", 0.989552207, 345]
     
    
How to run:
    $ python 12_find_similar_movie.py --items=src-files/ml-100k/u.item src-files/ml-100k/u.data > sims.txt
    
### How can Improve it?

Some ideas:

    - Discard bad ratings
    - Try different metrics (Pearson Correlation Coefficient, Jaccard Coefficient, Conditional Probability)
    - Adjust the thresholds for minimum co-rates or minimum score
    - Invent a new similarity metric that take the number of co-raters into account
    - Use genre information in u.items to boost scores from movies in the same genre


# Apache Hadoop 

Hadoop is a framework built with Java for distributing computing. It's what lets you run MapReduce jobs on a cluster of cheap computers,
 instead of just one, offering redundancy and scalability.

Remember: alwsays assume that the script will works on different computers! This is very important, so pay attention!

## HDFS: Hadoop Distributed File System

https://en.wikipedia.org/wiki/Apache_Hadoop
http://hortonworks.com/hadoop/hdfs/
http://....

## Hadoop YARN

Hadoop YARN is how MapReduce V2 manages resources across a cluster, it's part of hadoop!

Check the website for more information!

https://hadoop.apache.org/docs/r2.7.1/hadoop-yarn/hadoop-yarn-site/YARN.html

CLIENT -- Resource Manager --> Node1 Manager --> Node2 Manager --> Node3 Manager

YARN is a funamental part of Hadoop, It works with HDFS to get its data, but YARN is how the work on MapReduce job gets split up anda managed.


# Connect MRJob to Amazon EMR

First of all you need an account on Amazon AWS. When the account is ready you have to follow this steps:

    - Go under section "Security Credentials"
    - Create new Access Key
    - Create on your env two new variables
    - export AWS_ACCESS_KEY_ID=YYY
    - export AWS_SECRET_ACCESS_KEY=XXX
    
To execute our MapReduce job on Amazon we can simply use our terminal:

    $ Single machine (will be very slow!)
    $ python 12_find_similar_movie.py -r emr --items=src-files/ml-100k/u.item src-files/ml-100k/u.data > sims.txt
    $ Multiple instances
    $ python 12_find_similar_movie.py -r emr --num-ec2-instances 4 --items=src-files/ml-100k/u.item src-files/ml-100k/u.data > sims.txt

To use as input / output S3 you can change the input / output target:

    $ python 12_find_similar_movie.py -r emr --num-ec2-instances 4 --items=src-files/ml-100k/u.item s3://YOUR-BUCKET/FOLDERS/u.data --output-dir=s3://YOUR-BUCKET/FOLDERS

## Troubleshooting

Is possible to monitoring the jobs from your terminal:
 
    $ Troubleshooting EMR jobs (subsitute your job ID):
    $ python -m mrjob.tools.emr.fetch_logs --find-failure j-JOBID

Or is possible also from AWS Dashboard (be sure to moved you location to UE East, N. Virginia):

    - On S3 section you can check the logs
    - On EMR you can check the status of the jobs

More detail here: https://pythonhosted.org/mrjob/guides/emr-quickstart.html

## Exercise: Scaled Up!

Let's try with a bigger dataset, 1M entries. Check the file 13_find_similar_movie_large.py. Is just like the 
exercise 12 but with a simple differents on how we load the movie names and the ratings file (different data format).

Let's try with 20 nodes on EMR!

    $ python 13_find_similar_movie_large.py -r emr --num-ec2-instances=20 --items=src-files/ml-1m/movies.dat src-files/ml-1m/ratings.dat > sims-1ml.txt
    
## Be careful

When we'll use multiple nodes we'll have some problems with the sort job due to multiple instances of reducer. So, if we'll use 4 machines, we'll have 4 grouped result sorted. 
We have to manage manually this problem, for example adding a separated MapReduce job after the end of those steps. 
 
For example, after job **13_find_similar_movie_large.py** we can apply the script **14_starwars_sims.py** to find the hottest results!

    $ python 14_starwars_sims.py sims-1ml.txt > starwars_sims.txt
    
# Programmatically Running Jobs

To run programmatically a job is possible use the **MrJob Runners**, which permit to start the execution and read the output. 
If we imagine to call some MapReduce job from another software we'll use an istance of Runner that will run the job for us. We can see an example under folder 
**src/05-mrjob-runners/**.

Our runner for the word_count job will looks like:

```
from wordcount import MRWordFrequency

mr_job = MRWordFrequency()
mr_job.stdin = open('utils/04_book.txt')

with mr_job.make_runner() as runner:
        runner.run()
        for line in runner.stream_output():
            key, value = mr_job.parse_output_line(line)
            print "Word: ", key, " Count: ", value
```
    
The **stdin** is where actually mrjob will receive the input, in this case from a file on my pc. 
Then the runner will provide back the output through the **stream_output** function, which is a generator that returns a single HadoopStreaming output line,
so we need to call **parse_output_line** to get back the emitted key and value.

How to run:

    $ python src/05-mrjob-runners/mrjob_runner.py
    
## Return Json

Thanks to our runner is possibile to evaluate the result and create a json / csv as result instead of a simple row. Check the example **mrjob_runner_ver2.py** to see how it's made!

# Web Server Integration

Folder **06-webserver** contains a collection of examples and how-to related on how integrate map reduce and visualization with a Python simple server. 
I'm using Turbogears2 (http://turbogears.org) as framework, Jinja2 as template engine (http://jinja.pocoo.org/) and D3js (http://d3js.org) to create simple visualization.

Here a quick resume on each example, you can use the file **requirements.txt** to install what you need.

### 01-simple-server

Is a very dummy version of a simple server made with Python using WSGI.

### 02-tg2-simple-server

As the example before, is a simple server built with Turbogears.

### 03-templating-jinja

In this example is showed how to return through a simple server with TG2 an HTML page correlated with some parameters. 
There is also a simple javascript file used to draw a line graph to show the data received (In this case CPU usage).
 
### 04-serving-json

Is similar to example 03, but is in real time bro! There is an API on **/data** that response with a json like:

    {
        usage: 24.4
    }

I changed the script to retrieve automatically and forever data from the API.

### 05-tg2-mapreduce

This is the most interesting example of how to connect a mapreduce job to a web server. In this case the API will use a custom **mrjob runner** to 
apply map and reduce wordcount on an defined text. As output will be show the amount of occurrences of each letter in a bar graph using D3js.
