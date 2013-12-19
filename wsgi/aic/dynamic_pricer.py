import db
import datetime as dt
import settings
import crowd
import math


if __name__ == '__main__':
	print("Start updating bonus")
	print(len(settings.bonus_matrix))
	
	for x in range(0, len(settings.bonus_matrix)):
		print(x)
		session = db.Session()
		if x == len(settings.bonus_matrix)-1:
			print("if")
			query = session.query(db.Task).filter(db.Task.datetime < (dt.datetime.now() - dt.timedelta(days=settings.bonus_matrix[x][0]))).filter(db.Task.datetime > (dt.datetime.now() - dt.timedelta(days=settings.delete_time))).filter(db.Task.finished_rating == None).filter(db.Task.garbage_flag == False)
		else:
			print("else")
			query = session.query(db.Task).filter(db.Task.datetime < (dt.datetime.now() - dt.timedelta(days=settings.bonus_matrix[x][0]))).filter(db.Task.datetime > (dt.datetime.now() - dt.timedelta(days=settings.bonus_matrix[x+1][0]))).filter(db.Task.finished_rating == None).filter(db.Task.garbage_flag == False)
		tasks = query.all()
		for task in tasks:
			print("__"+str(task.id))
			new_bonus = math.ceil(settings.bonus_matrix[x][1] * task.price *100)/ 100
			if new_bonus != task.price_bonus:
				task.price_bonus = new_bonus
				crowd.set_bonus(task)
				print("-set bonus of task " +str(task.id) + " to " + str(task.price_bonus))
				session.commit()

	print("Finished updating bonus")
