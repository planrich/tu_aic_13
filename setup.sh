
sudo apt-get install git python python-dev python-pip postgresql-9.1 python-psycopg2 python-lxml python-numpy python-requests python-sqlalchemy

mkdir aic
cd aic
git clone https://github.com/planrich/tu_aic_13.git main
git clone https://github.com/planrich/tu_aic_crowd_source.git crowd

sudo python crowd/setup.py install
sudo python main/setup.py install

echo "create role aic with password 'aic';" | sudo -u postgres psql
sudo -u postgres createdb -O aic aic
