
sudo apt-get -y install git python python-dev python-pip postgresql-9.1 python-psycopg2 python-lxml python-numpy python-requests python-sqlalchemy

mkdir -p aic
cd aic
git clone https://github.com/planrich/tu_aic_13.git main
git clone https://github.com/planrich/tu_aic_crowd_source.git crowd

sudo python crowd/setup.py install
sudo python main/setup.py install
mkdir -p main/logs

echo "create user aic with password 'aic'; create database aic owner aic;" | sudo -u postgres psql 
