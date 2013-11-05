

import db



session = db.Session()

p = db.Project("paragraph", "http", 0)


session.add(p)
session.commit()

t = db.Task(p,"apple", "paragraph")
session.add(t)
session.commit()

print(t.project_id)


session = db.Session()

projs = session.query(db.Project).all()

for proj in projs:
    print ("%d id" % proj.id)
    print(proj.finishedRating == None)

    for task in proj.tasks:
        print("   has task %d" % task.id)


import random
w = db.Worker("abcdef" + str(random.randint(0,1000000000)))
session.add(w)
session.commit()

a = db.Answer(t, w, 0) 
session.add(a)
session.commit()

for _a in w.answers:
    if _a.id == a.id:
        print("found")





