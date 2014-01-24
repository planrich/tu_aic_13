import os
import numpy as np
import logging

RSS_URL = 'http://finance.yahoo.com/news/?format=rss'
SECRET_KEY = "kl12kCF(uL>ASJ123r5b129cfujxzl;kjashb124e12edljcv"

#Settings for application service
#Date format in keyword queries (eg. 2013-12-31)
DATE_FORMAT_KEYWORD = '%Y-%m-%d'
#Number of ratings per page
PAGE_SIZE_KEYWORD = 20



# bonus_matrix: each row is a bonus step
# bonus_matrix: in column 0 is the time when the bonus is active (5 means the bonus is set after 5 days)
# bonus_matrix: in column 1 is the bonus value (0.25 means the bonus is 25 per cent of the normal price)
bonus_matrix = np.array([[4, 0.25],[8, 0.5]])
#bonus_matrix[0][0] = 4
#bonus_matrix[0][1] = 0.25
#bonus_matrix[1][0] = 8
#bonus_matrix[1][1] = 0.5

# after this number of days a unsolved task gets deleted
delete_time = 10

production = os.environ.get('OPENSHIFT_POSTGRESQL_DB_URL') is not None

if production:
    DB_URL = os.environ.get('OPENSHIFT_POSTGRESQL_DB_URL')
    DOMAIN = 'http://main-tuaic13.rhcloud.com'
    CROWD_DOMAIN = 'http://crowd-tuaic13.rhcloud.com'
else:
    DB_URL = 'postgresql://aic:aic@localhost/aic'
    DOMAIN = 'http://127.0.0.1:5000'
    CROWD_DOMAIN = 'http://127.0.0.1:5001'


def createLog(name):
	logger = logging.getLogger(name)
	logger.setLevel(logging.INFO)
	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	console = logging.StreamHandler()
	console.setLevel(logging.INFO)
	console.setFormatter(formatter)
	logger.addHandler(console)
	if production:
<<<<<<< HEAD
		path = os.environ.get('OPENSHIFT_TMP_DIR/logs/')
		logFile = logging.FileHandler(filename=path+name+'.log')
=======
		logFile = logging.FileHandler(filename='app-root/repo/logs/'+name+'.log')
>>>>>>> cc823eace74efbea76ef780cce3ddac9ed1b4983
	else:
		logFile = logging.FileHandler(filename='logs/'+name+'.log')
	
	logFile.setLevel(logging.INFO)
	logFile.setFormatter(formatter)
	logger.addHandler(logFile)
	return logger