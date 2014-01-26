# AIC WS 2013

This app also depends on the application located at: https://github.com/planrich/tu_aic_crowd_source.

# Installation - Ubuntu 12.04

The following setup instructinos has been tested in virtual box using the 32 bit
ubuntu 12.04 lts version.

## Fully automated

This script contains sudo statements to install software.

~~~
wget -q -O - https://raw.github.com/planrich/tu_aic_13/master/setup.sh | sh
~~~

## In more detail

dependencies:

~~~
git (1:1.7.9.5-1)
python (2.7.3)
python-dev (2.7.3)
python-pip (1.0-1build1)
python-flask (0.8-1)
python-psycopg2 (2.4.5-1)
python-lxml (2.3.2-1)
python-numpy (1:1.6.1-6ubuntu1)
python-requests (0.8.2-1)
python-sqlalchemy (0.7.4-1ubuntu0.1)
postgresql-9.1 (9.1.11-0ubuntu0.12.04)
~~~

on ubuntu 12.04 LTS do the following:
~~~
sudo apt-get install git python python-dev python-pip postgresql-9.1 python-psycopg2 python-lxml python-numpy python-requests python-sqlalchemy
~~~

now clone the repository by issueing the following commands:

~~~
mkdir aic
cd aic
git clone https://github.com/planrich/tu_aic_13.git main
git clone https://github.com/planrich/tu_aic_crowd_source.git crowd
~~~

There are some dependencies that are not included in the ubuntu repository. Thus issue the two commands

~~~
sudo python crowd/setup.py install
sudo python main/setup.py install
~~~

Setup the database user and create the database:

~~~
echo "create user aic with password 'aic'; create database aic owner aic;" | sudo -u postgres psql
~~~

# Try it out

Open two shells and type `make run` in the two folders (crowd,main).
Not the crowdsourcing app runs at `127.0.0.1:5001` and the sentiment app on
`127.0.0.1:5000`.

You can look at the Makefiles so see which commands you can issue.

## Sentiment app Makefile

in more detail!

# Setup for development

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

# Postgres

You should have a postgres instance up and running and login as root:

~~~
postgres@localhost$ psql
postgres=#
~~~

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

# The idea

Task is a question "Keyword mentioned bad/neutral/negative in this paragrpah"
We aggrate the answers of workers only when a task is complete. Before the aggregation we should find
bad workers.
