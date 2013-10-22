import os

DB = {
  'database': os.environ.get('AIC_DB_NAME', 'aic'),
  'user': os.environ.get('AIC_DB_USER', 'aic'),
  'password': os.environ.get('AIC_DB_PASSWORD', 'aic'),
  'host': os.environ.get('AIC_DB_HOST', '127.0.0.1')
}

RSS_URL = 'http://finance.yahoo.com/news/?format=rss'