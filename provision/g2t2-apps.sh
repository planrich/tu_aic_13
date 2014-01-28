#!/bin/bash

echo "Initial apt-get update ..."
apt-get update >/dev/null

echo "Installing required packages ..."
apt-get -y install make git python python-dev python-pip postgresql-9.1 \
	python-psycopg2 python-lxml python-numpy python-requests curl \
	python-sqlalchemy language-pack-de language-pack-en vim-nox >/dev/null

echo "Creating database ..."
echo "create user aic with password 'aic'" | sudo -u postgres -H psql >/dev/null
sudo -u postgres -H createdb --locale=en_US.utf8 -E UTF-8 -T template0 -O aic aic > /dev/null

mkdir /home/vagrant/aic

echo "Installing Main app ..."
git clone https://github.com/planrich/tu_aic_13.git /home/vagrant/aic/main >/dev/null
cd /home/vagrant/aic/main
python setup.py install >/dev/null

echo "Installing Crowd app ..."
git clone https://github.com/planrich/tu_aic_crowd_source.git /home/vagrant/aic/crowd >/dev/null
cd /home/vagrant/aic/crowd
python setup.py install >/dev/null

chown -R vagrant:vagrant /home/vagrant/aic

echo "Installing Upstart jobs ..."
cp /vagrant/provision/upstart/*.conf /etc/init/

echo "Starting Main app ..."
start g2t2-main

echo "Starting Crowd app ..."
start g2t2-crowd

echo "Importing demo data into Main app ..."
cd /home/vagrant/aic/main
make demo_set_db >/dev/null

echo "Importing demo data into Crowd app ..."
cd /home/vagrant/aic/crowd
make demo_set_db >/dev/null

echo ""
echo "Main and Crowd app Vagrant-based setup complete."
echo ""
echo "- Main:  http://g2t2-apps.vm:5000"
echo "- Crowd: http://g2t2-apps.vm:5001"
echo ""
