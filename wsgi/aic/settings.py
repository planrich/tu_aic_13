import os



DB_URL = os.environ.get('DB_URL', 'postgresql://aic:aic@localhost/aic')
if os.environ.get('OPENSHIFT_POSTGRESQL_DB_URL') is not None:
    DB_URL = os.environ.get('OPENSHIFT_POSTGRESQL_DB_URL', 'postgresql://aic:aic@localhost/aic')

RSS_URL = 'http://finance.yahoo.com/news/?format=rss'
SECRET_KEY = "kl12kCF(uL>ASJ123r5b129cfujxzl;kjashb124e12edljcv"
mobileWorks_Username = 'aic13lab2topic2'
mobileWorks_Password = '1diesgp1'
mobileWorks_Webhook = 'http://aic13lab2topic2-mobileworks.rhcloud.com/webhook'
