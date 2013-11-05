AIC 13
=========

# Setup

You must also setup https://github.com/planrich/tu_aic_crowd_source using the same commands below to get this working.

recommended structure:
aic:
  crowd -> https://github.com/planrich/tu_aic_crowd_source
  main -> https://github.com/planrich/tu_aic_13

To get started you need pip (optionally virtualenv) installed.

## virtualenv

Virtual env is a way to manage the pip packages locally.
You simply execute the following:

~~~
$ virtualenv venv/
~~~

This creates a venv/ folder.
Then before you can install packages and run the application you must 
activate the environment in venv/

~~~
$ source venv/bin/activate
(venv) $
~~~

Then to install the dependencies:

~~~
(venv) $ pip install -r requirements.txt
~~~

## Without virtualenv

~~~
$ pip install -r requirements.txt
~~~

An pip will try to install the dependencies into the global package directory. 
On most setups it is required to be root to issue this command.

## Start the development webserver

After you have installed the requirements you can simple issue:

~~~
(env) crowd $ python wsgi/aic/app.py
 * Running on http://127.0.0.1:5001/
 * Restarting with reloader
~~~

~~~
(env) main $ python wsgi/aic/app.py
 * Running on http://127.0.0.1:5000/
 * Restarting with reloader
~~~

The crowd webapp runs on 5001 and the normal main app runs on port 5000!

# Postgres

You should have a postgres instance up and running and login as root:

~~~
$ psql
rich=#
~~~

in my case the username is rich and the # shows that i'm root user.

Then create the user and database:

~~~
rich=# create user aic with password 'aic';
CREATE ROLE
rich=# create database aic owner aic;
CREATE DATABASE
~~~

Reset the database:

~~~
rich=# drop database aic; create database aic owner aic;
DROP DATABASE
CREATE DATABASE
~~~

Then you might consider popolating keywords before scaping:

~~~
(venv) main $ python wsgi/aic/insert_keywords.py
(venv) main $ python wsgi/aic/scraper.py
~~~

# The idea

Task is a question "Keyword mentioned bad/neutral/negative in this paragrpah"
We aggrate the answers of workers only when a task is complete. Before the aggregation we should find
bad workers.


# The old idea

To decide on how to implement this assignment I would like to take the view of a customer:

When I use our final product, as I customer I would like to see the following:

~~~
+------------------------------------------------------+
|                                                      |
|                        +---------------------+       |
| Enter company/product: | Apple               |       |
|                        +---------------------+       |
|                                                      | 
|                        +---------------------+       |
| Trend in the last:     | v  3 months         |       |
|                        +---------------------+       |
|                                                      | 
|                        Show results                  | 
|                                                      |
+------------------------------------------------------+
~~~

Then the result could look like the following:

~~~
+------------------------------------------------------+
|                                                      |
| In the last 3 months Apple has been mentioned        |
| in 1324 of all 23000 articles.                i
| It has been mentioned 234124 since the start of the  |
| service. (234124/1324 = 17.7%)                       |
|                                                      |
| The sentiment in the last 3 months was: 45%          |
| +--------------------------------------------------+ |
| |********************                              | |
| +--------------------------------------------------+ |
| bad                  neutral                   good  |
|                                                      |
|                                                      |
| The overall sentiment is: 72%                        |
| +--------------------------------------------------+ |
| |************************************              | |
| +--------------------------------------------------+ |
| bad                  neutral                   good  |
|                                                      |
| What do people say about Apple in the last three     |
| months:                                              |
|                                                      |
| "Apple has released a new iPhone" <link>             | // link to finance article
| "Appels App-Store loses Developers" <link>           |
| "The good news is that Apple again kicks &@#" <link> |
| ...                                                  |
| ...                                                  |
|                                                      |
+------------------------------------------------------+
~~~

First how is the sentiment calculated:

My idea is to take a survey approach. We have these workers that complete
difficult tasks. A computer cannot do it that easy. Therefore we supply
this task x times. (x > 1). Lets say x = 3. Then 
every worker has to supply the following:

Which companies/products are mentioned in this text and supply
a number in [0..10] for every company about the sentiment.
For example 0 would be very bad sentiment. The author seems to
hate the product/company.
5 would be neutral. The company/product exists.
10 would be that it is a really good product/company and you should buy the 
product or their products.

Additionally to punctuate our sentiment calculation the worker
should provide short sentences about the company/product.
Depending on the restriction I would suggest that the sentence
must contain the name of the product/company.

After all we then have x answers from x workers. (e.g 3)
Here I think it is easy to find black sheeps. When
1 of 3 workers do not provide the same amount of companies
and the sentiment is quite different then this might indicate
that the worker should get another job. Thus this worker
is blacklisted. If this happens very often the blacklisted 
rank increases and after the rank hits a threshold the worker
cannot solve tasks anymore.
To check if the supplied sentences are really contained in
the finance article is a trivial task for a computer.

Additionally if we take the mean value of the provided answers
we could get a more "accurate" answer (worker could have bias on 
company/product).

Conflict resolution in product/company names:
1) As ther might be some problems with the name mapping I suggest
to provide a simple web interface for the human workers
where the can lookup the companies that already exist in our database.
So when they find a company, they enter the name and get a list
of results -> pick the most accurate, or if none exists just pick
the name in the article.
2) Create a routine that finds names that seem to be equal. Then you can
merge double entries by hand.


Apple, Facebook, Google, Microsoft, Yahoo, Oracle
iPhone, 


