import os

DB_URL = os.environ.get('DB_URL', 'postgresql://aic:aic@localhost/aic')
RSS_URL = 'http://finance.yahoo.com/news/?format=rss'