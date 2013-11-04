import os

RSS_URL = 'http://finance.yahoo.com/news/?format=rss'

# if deployed on openshift
if os.environ.get('OPENSHIFT_POSTGRESQL_DB_URL') is not None:
    DB_URL = os.environ.get('OPENSHIFT_POSTGRESQL_DB_URL', 'postgresql://aic:aic@localhost/aic')
    POST_TASK_LINK = 'http://aic13lab2topic2-mobileworks.rhcloud.com/tasks'
else:
	DB_URL = os.environ.get('DB_URL', 'postgresql://aic:aic@localhost/aic')
	POST_TASK_LINK = 'http://127.0.0.1:5000/tasks'
