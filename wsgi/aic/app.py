# encoding: utf-8
from flask import Flask, request, render_template
from flask.json import jsonify

import db
import settings
import utils


application = Flask(__name__)
application.secret_key = settings.SECRET_KEY


# WEBAPP
###########################################################

@application.route("/")
def index():
    #sess = db.Session()
    #pubs = sess.query(db.Publication).all()
    return render_template("index.html")


# API
###########################################################

@application.route("/api/task/<task_id>/answers", methods=['POST'])
def post_task_answer(task_id):
    session = db.Session()
    task = session.query(db.Task).filter(db.Task.id == task_id).first()
    if not task:
        return jsonify(error='Task not found'), 404

    raw_answer = utils.get_raw_answer(request)
    if not raw_answer:
        return jsonify(error='Error parsing json'), 400

    worker_id = raw_answer['user']
    worker = session.query(db.Worker).filter(db.Worker.id == worker_id).first()
    if not worker:
        worker = db.Worker(worker_id)
        session.add(worker)
        session.commit()

    answer = db.Answer(task, worker, raw_answer['answer'])
    session.add(answer)
    session.commit()

    if len(task.answers) == task.answers_requested:
        task.calculate_rating()
        session.add(task)
        session.commit()

    return jsonify(answer.as_dict()), 200


# TODO: Refactor this ---
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
