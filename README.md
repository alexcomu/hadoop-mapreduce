# Hadoop and Map Reduce

## Requirements

We need:

	- Python 2.7
	- Virtualenv (pip install virtualenv && virtuale envMyEnv && source envMyEnv/bin/activate) 
	- MrJob (pip install mrjob)
	- Download MovieData DB (100K) http://grouplens.org/datasets/movielens/ 
	- Put the unzip folder into src-movies folder


Check -> https://github.com/alexcomu/big-data-basics to read a simple introduction on MapReduce and Hadoop.


## Example

### 01_rating_counter.py

Count occurences of rating value from movie DB.

### 02_avarage_friends.py

Calculate For each Age the Avarage of friends. Data (csv) Structure:

	ID, Name, Age, Number of Friends

How to Run:

	$ python src/02_avarage_friends.py CSV-SOURCE.csv > result.txt


### 03_temperature_extreme.py

Check for each location the minimum or maximum temperature.

Src file:

     03_temperature.csv

How to Run:

     $ python src/03_temperature_extreme.py CSV-SOURCE.csv > result.txt
     
     
### 04_word_frequency.py

Calculate the word frequency from a book source.

How to Run:

     $ python src/04_word_frequency.py CSV-SOURCE.csv > result.txt

### 04_word_frequency_orderBy_frequency.py

Calculate word frequency and then order the list by frequency using 2 MapReduce Jobs in series.

The Input of the second job will be the output of the first one, so the second Map function will sort the result of the first reducer by occurrences and the second Reducer will only print the result.

How to Run:

     $ python src/04_word_frequency_orderBy_frequency.py CSV-SOURCE.csv > result.txt

### 05_total_spend_by_customer.py

For each customer from an input file (05_customer_order.csv) extract how much he spent.

How to Run:

     $ python src/05_total_spend_by_customer.py CSV-SOURCE.csv > result.txt
     
     
