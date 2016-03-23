# Hadoop and Map Reduce

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

### 01_most_rated_movie

Count occurrences of each movie rating from movie DB and find the most rated movie.

### 02_quick_lookup

Add to the previous example the name of the movie, readed from u.item file using **configure_options** and **reducer_init**!

How to Run:

     $ python src/02-advanced-mapreduce/02_quick_lookup.py --items=PATH-TO-u.ITEM PATH-TO-u.DATA > result.txt

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

