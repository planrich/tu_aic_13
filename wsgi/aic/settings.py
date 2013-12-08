import os

RSS_URL = 'http://finance.yahoo.com/news/?format=rss'
SECRET_KEY = "kl12kCF(uL>ASJ123r5b129cfujxzl;kjashb124e12edljcv"

#Settings for application service
#Date format in keyword queries (eg. 2013-12-31)
DATE_FORMAT_KEYWORD = '%Y-%m-%d'
#Number of ratings per page
PAGE_SIZE_KEYWORD = 20

bonus1_time = 5
bonus1_value = 0.25

production = os.environ.get('OPENSHIFT_POSTGRESQL_DB_URL') is not None

if production:
    DB_URL = os.environ.get('OPENSHIFT_POSTGRESQL_DB_URL')
    DOMAIN = 'http://main-tuaic13.rhcloud.com'
    CROWD_DOMAIN = 'http://crowd-tuaic13.rhcloud.com'
else:
    DB_URL = 'postgresql://aic:aic@localhost/aic'
    DOMAIN = 'http://127.0.0.1:5000'
    CROWD_DOMAIN = 'http://127.0.0.1:5001'
