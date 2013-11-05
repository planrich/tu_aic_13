# encoding: utf-8
from flask import Flask, request, render_template, json, flash, redirect, url_for, session
import platform
import db
import os
import settings
from sqlalchemy.orm.exc import NoResultFound

application = Flask(__name__)
application.secret_key = settings.SECRET_KEY

@application.route("/")
def index():
    #sess = db.Session()
    #pubs = sess.query(db.Publication).all()

    return render_template("index.html")

@application.route("/solve_task", methods=["POST","GET"])
def solve_task():
    sess = db.Session()
    if request.method == "POST":
        if "answer" not in request.form:
            flash("Task was not rated. No answer provided. Here is a new task!", "danger")
            return redirect(url_for("solve_task",r="t"))

        if "user_id" not in request.form:
            flash("You did not provide your user_id. Here is a new task! Try again.", "danger")
            return redirect(url_for("solve_task",r="t"))
        
        if "task_id" not in request.form:
            flash("Internal failure. Here is a new task!", "danger")
            return redirect(url_for("solve_task",r="t"))

        answer = request.form["answer"]
        task_id = request.form["task_id"]
        user_id = request.form["user_id"]

        if user_id is None or user_id.strip() == "":
            flash("You did not provide your user_id. Here is a new task! Try again.", "danger")
            return redirect(url_for("solve_task",r="t"))

        session['user_id'] = user_id

        try:
            task = sess.query(db.OpenTask).filter(db.OpenTask.id == task_id).one()
        except NoResultFound:
            flash("Internal failure. Here is a new task!", "danger")
            return redirect(url_for("solve_task",r="t"))

        # TODO request.get callback url with answer!
        task.solved = True
        sess.commit()

        requests.get("")

        flash("Solved task. Here is a new one!", "success")
        return redirect(url_for("solve_task",r="t"))
    else:
        try:
            task = sess.query(db.OpenTask).filter(db.OpenTask.solved == False).one()
        except NoResultFound:
            task = None

        user_id = session.get("user_id") or ""
        return render_template("solve_task.html", task=task, user_id=user_id)



@application.route("/list_tasks", methods=['GET'])
def list_tasks():
    sess = db.Session()
    open_tasks = sess.query(db.OpenTask).all()
    return render_template("task_list.html", tasks = open_tasks)


def sanitize_post_task(json):
    if not json:
        print("fail")
        return None

    if not 'id' in json or\
       not 'task_description' in json or\
       not 'answer_possibilities' in json or\
       not 'callback_link' in json or\
       not 'price' in json:
       return None

    return json

@application.route("/tasks", methods=['POST'])
def task():
    j = sanitize_post_task(request.get_json(force=True,silent=True))
    if not j:
        return json.dumps({ 'error': 'provide a json body' }), 400

    session = db.Session()

    tid = j['id']
    if session.query(db.OpenTask).filter(db.OpenTask.id == tid).count() != 0:
        return json.dumps({ 'error': 'id already exists' }), 400

    answers = j['answer_possibilities']
    answer = None
    if type(answers) is type([]):
        answer = "|".join(answers)
    elif answers == 'text':
        answer = "text"
    else:
        return json.dumps({ 'error': 'answer_possibilities must either be of type list ["yes","no",...] or "text"' }), 400

    open_task = db.OpenTask(j['id'], j['task_description'], answer, j['callback_link'], j['price'])
    session.add(open_task)
    session.commit()

    result = { 'error': None, 'success': True }

    return json.dumps(result), 200

@application.route("/webhook", methods=['GET', 'POST'])
def webhook():
    folder = os.environ['OPENSHIFT_TMP_DIR']
    if request.method == 'POST':
        data = str(request.stream.read())
        f = open(folder+'/datafile','a')
        f.write(data + ' ### ')
        return '<h1>' + data +'</h1>'

    f = open (folder+'/datafile', 'r')
    return '<p>'+ f.read() +'</p>'
    
@application.route('/query/<company>', defaults={'timespan': 999999})
@application.route("/query/<company>/<int:timespan>")
def query(company, timespan):
    out=''
    sess = db.Session()
    tasks = sess.query(db.Keyword, db.Task, db.Project).filter \
        (db.Keyword.keyword==company \
        # and db.Project.finishedRating != None \  does not work
        and db.projects.datetime > date.today - timespan)
    cnt=0
    total=0
    for k,t,p in tasks:
        if p.finishedRating == None:
            continue
        cnt+=1
        total+=int(p.finishedRating or 0)
        out += str(total)
    if cnt == 0:
        return '{}'
    return '{"'+company+ '":' + str(1.0*total/cnt) + '}'
	
if __name__ == "__main__":
    application.debug = True
    application.run()
