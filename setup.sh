
sudo apt-get -y install make git python python-dev python-pip postgresql-9.1 python-psycopg2 python-lxml python-numpy python-sqlalchemy

mkdir -p aic
cd aic
git clone https://github.com/planrich/tu_aic_13.git main
git clone https://github.com/planrich/tu_aic_crowd_source.git crowd

sudo python crowd/setup.py install
sudo python main/setup.py install
mkdir -p main/logs

echo "create user aic with password 'aic';" | sudo -u postgres psql
sudo -u postgres -H createdb --locale=en_US.utf8 -E UTF-8 -T template0 -O aic aic
