import db
import datetime as dt
import settings
import crowd
import math


if __name__ == '__main__':
	print("Start updating bonus")
	
	session = db.Session()
	query = session.query(db.Task).filter(db.Task.datetime < (dt.datetime.now() - dt.timedelta(days=settings.bonus1_time)))
	tasks = query.all()
	for task in tasks:
		new_bonus = math.ceil(settings.bonus1_value * task.price *100)/ 100
		if new_bonus != task.price_bonus:
			task.price_bonus = new_bonus
			crowd.set_bonus(task)
			print("-set bonus of task " +str(task.id) + " to " + str(task.price_bonus))
	session.commit()
