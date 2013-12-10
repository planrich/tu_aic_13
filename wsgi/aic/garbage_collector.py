import db
import datetime as dt
import settings
import requests
import crowd




if __name__ == '__main__':
	print("Starting garbage collector")

	session = db.Session()
	query = session.query(db.Task).filter(db.Task.datetime < (dt.datetime.now() - dt.timedelta(days = settings.delete_time))).filter(db.Task.finished_rating == None).filter(db.Task.garbage_flag == False)
	tasks = query.all()
	for task in tasks:
		status = crowd.set_garbage(task)
		if status == requests.codes.ok:
			task.garbage_flag = True
			session.commit()
			#print("task " + str(task.id) + " is now garbage")
		else:
			print("Error: Can not set task " + str(task.id) + " to garbage (Error " + str(status) + ")")
	print("Finished garbage collector")