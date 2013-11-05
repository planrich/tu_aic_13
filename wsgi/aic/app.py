# encoding: utf-8
from flask import Flask, request, render_template, json, flash, redirect, url_for, session
import platform
import db
import os
import settings
import requests

from sqlalchemy.orm.exc import NoResultFound
from requests.exceptions import Timeout

application = Flask(__name__)
application.secret_key = settings.SECRET_KEY

@application.route("/")
def index():
    #sess = db.Session()
    #pubs = sess.query(db.Publication).all()

    return render_template("index.html")

def valid_webhook_json(json):
    if not json:
        return None

    if not 'id' in json or\
       not 'answer' in json or\
       not 'user' in json:
       return None

    return json

@application.route("/webhook", methods=['POST'])
def webhook():
    data = valid_webhook_json(request.get_json(force=True,silent=True))
    if not data:
        return "{error:'did not provide valid data!'}", 400

    task_id = int(data['id'].split("_")[0])
    print("task_id", task_id)
    answer = data['answer']
    worker_id = data['user']

    session = db.Session()
    task = None
    worker = None
    try:
        task = session.query(db.Task).filter(db.Task.id == task_id).limit(1).one()
    except NoResultFound:
        return "{'error':'invalid task id'}",400

    try:
        worker = session.query(db.Worker).filter(db.Worker.id == worker_id).limit(1).one()
    except NoResultFound:
        worker = db.Worker(worker_id)
        session.add(worker)
        session.commit()

    rating = -1
    if answer.lower() == "positive":
        rating = 10
    elif answer.lower() == "neutral":
        rating = 5
    elif answer.lower() == "negative":
        rating = 0

    if rating == -1:
        return ("{'error':'answer must be positive,neutral or negative but it is %s'}" % answer),400

    answer = db.Answer(task, worker, rating)
    session.add(answer)
    session.commit()
    
    # TODO check if project is finished!

    return "{'error':null,'status': 'ok'}", 200
    
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
