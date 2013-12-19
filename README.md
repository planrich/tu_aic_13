# Setup

You must also setup https://github.com/planrich/tu_aic_crowd_source using the same commands below to get this working.

recommended structure:
~~~
aic/
  crowd/-> https://github.com/planrich/tu_aic_crowd_source
  main/ -> https://github.com/planrich/tu_aic_13
~~~

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