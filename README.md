AIC 13
=========



## An idea (rich)

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
| 1324 times.                                          |
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
difficult tasks. A computer cannot do it that easily. Therefore we supply
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

