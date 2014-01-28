# AIC WS 2013

This app also depends on the application located at: https://github.com/planrich/tu_aic_crowd_source.

# Operating system
Ubuntu 12.04 lts (tested with 32 bit version in virtual box)

# Fully automated installation

## Option 1: Using Vagrant

We provide a Vagrantfile and accompanying provisioning scripts to create an
Ubuntu 12.04 VM (VirtualBox) and install and deploy the main and crowd
applications. This requires VirtualBox, Vagrant and the Vagrant Hostmanager
plugin. The Hostmanager plugin updates your the VM's and your local
`/etc/hosts` file with the name and address of the newly provisioned VM.

* VirtualBox: https://www.virtualbox.org/wiki/Downloads
* Vagrant: http://www.vagrantup.com/downloads.html

After Vagrant is installed get the vagrant-hostmanager plugin:

~~~
vagrant plugin install vagrant-hostmanager
~~~

Clone this repository:

~~~
git clone https://github.com/planrich/tu_aic_13
cd tu_aic_13
~~~

To add a vagrant box, enter the following line:

~~~
vagrant box add precise64 http://files.vagrantup.com/precise64.box
~~~

Now simply run:

~~~
vagrant up
~~~

After a few minutes a new VirtualBox VM named "g2t2-apps.vm" will be
running the main and crowd applications.

Now point your browser to:

* Main: http://g2t2-apps.vm:5000
* Crowd: http://g2t2-apps.vm:5001

Various warnings issued during Vagrant provisioning when installing the
applications or importing demo data can be ignored.

To connect to the VM via SSH:

~~~
vagrant ssh
~~~

The applications are managed as Upstart tasks so you can use `start`, `stop`,
`restart` and `status` or their `service` equivalents inside the VM:

~~~
status g2t2-main
restart g2t2-crowd
...
~~~

To shutdown and remove the VM:

~~~
vagrant destroy -f
~~~

## Option 2: On the local machine

Use the `setup.sh` script to install the main and crowd applications on your local machine:

~~~
wget -q -O - https://raw.github.com/planrich/tu_aic_13/master/setup.sh | sh
~~~

# Manual installation

## Required software
* git - 1:1.7.9.5-1 - `sudo apt-get install git`
* python - 2.7.3 - `sudo apt-get install python`
* python-dev - 2.7.3 - `sudo apt-get install python-dev`
* python-pip - 1.0-1build1 - `sudo apt-get install python-pip`
* python-flask - 0.8-1 - `sudo apt-get install python-flask`
* python-psycopg2 - 2.4.5-1 - `sudo apt-get install python-psycopg2` 
* python-lxml - 2.3.2-1 - `sudo apt-get install python-lxml`
* python-numpy - 1:1.6.1-6ubuntu1 - `sudo apt-get install python-numpy`
* python-requests - 0.8.2-1 - `sudo apt-get install python-requests`
* python-sqlalchemy - 0.7.4-1ubuntu0.1 - `sudo apt-get install python-sqlalchemy`
* postgresql-9.1 - 9.1.11-0ubuntu0.12.04 - `sudo apt-get install postgresql-9.1`

## Setup scripts
clone the repository by issuing the following commands:

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

# Run the application

Open two shells and type `make run` in the two folders (crowd,main).
Now the crowdsourcing app runs at `127.0.0.1:5001` and the sentiment app on
`127.0.0.1:5000`.
Please consider that the database is empty and you won't get any sentiment when you query the main app. Also you won't see any open tasks on the crowd app as it takes up to one hour until the Advanced Python Scheduler starts the first scraping of the articles. If you want to see how the application works use the prepared demo data. (see next section)

#Available features

## Fill the database with demo data
We have prepared some data that you can see how the application works. To fill the data in the database open two shells and type `make demo_set_db` in the two folders (crowd, main)

## Start the application in demo mode
The application has a demo mode. In contrast to the normal mode where the scraping of articles, dynamic pricing of tasks and garbarge collection of tasks is started hourly by the Advanced Python Scheduler you can start this things per hand in the demo mode. To start the application in demo mode open two shells and type `make demo_run` in the two folders (crowd, main).

## Query the sentiment (the application must run in demo mode)
Open `127.0.0.1:5000` with firefox and enter your search. (eg. Microsoft)

## Manage the sentiment, workers and keywords (the application must run in demo mode)
Open `127.0.0.1:5000` with firefox and klick on the gear-wheel. There you have the menu point Open tasks to get an overview of the open tasks, the menu point workers to manage your workers and the menu point keywords to manage the keywords.

## Solve tasks (the application must run in demo mode)
Open `127.0.0.1:5001` with firefox. You can see a list with all tasks that should be solved. Choose one an click on solve, enter your worker ID, read the text, answer the question and click on send solution.

## Start the scraper (to get new tasks based on the articles; the application must run in demo mode)
Open a new shell in main and type `make demo_run_scraper`. You can then see the new tasks in the crowd(Open `127.0.0.1:5001` with firefox, go to the last page) and the main(Open `127.0.0.1:5000` with firefox, klick on the gear-wheel, go to the last page) app.

## Start the garbage collection (the application must run in demo mode)
There are some tasks in the demo data that are older than 10 days. You can then see this tasks in the crowd(Open `127.0.0.1:5001` with firefox) and the main(Open `127.0.0.1:5000` with firefox, klick on the gear-wheel) app. Open a new shell in main and type `make demo_run_garbage_collector` to delete this tasks. If you check the crowd or the main app after this tasks are gone.

## Start the dynamic pricing (the application must run in demo mode)
There are some tasks in the demo data that are older than 4 respectively 8 but younger than 10 day. You can then see this tasks in the crowd(Open `127.0.0.1:5001` with firefox) and the main(Open `127.0.0.1:5000` with firefox, klick on the gear-wheel) app. Open a new shell in main and type `make demo_run_dynamic_pricer` to give this tasks a bonus of 0.25 respectively 0.5 percent of the normal price.

## Block bad worker (the application must run in demo mode)
When you open `127.0.0.1:5000` with firefox, klick on the gear-wheel and klick on workers you can see all your workers. All workers have a rating that is decresed on bad performance. If a worker reaches the rating -20 it is automatically blocked. In this overview you can manually block/unblock workers by clicking on the button.

## Run scraper, garbage collection and dynamic pricing with the Advanced Python Scheduler hourly (the application must run in demo mode)
Open a shell in main an type `make demo_run_scheduler`. Please consider that it takes up to one hour until the first run of the scraper, garbage collection and dynamic pricing.

# Reset the database
You can reset the database (eg to delete the demo data and use the application with real data). Therefor you have to open a shell in main an type `make reset_db`

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

Task is a question "Keyword mentioned bad/neutral/negative in this paragraph"
We aggrate the answers of workers only when a task is complete. Before the aggregation we should find
bad workers.
