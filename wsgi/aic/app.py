# encoding: utf-8
from flask import Flask, request, render_template
from flask.json import jsonify

import db
import settings
import utils
import json
import datetime


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



@application.route('/keyword/<company>/')
def keyword_basic_info(company):
    output_basic_info={"keyword":"", "first_seen":"", "num_rating":0}
        
    sess=db.Session()
    tasks= sess.query(db.Keyword, db.Task, db.Project).filter \
        (db.Keyword.keyword==company,\
         db.Task.project_id==db.Project.id, \
        db.Task.keyword_id==db.Keyword.id\
        ).order_by(db.Project.datetime)
    output_basic_info["keyword"] = company
    output_basic_info["num_rating"] = tasks.count()
    for k,t,p in tasks:
        
        output_basic_info["first_seen"] = str(p.datetime)
        break
    
    return json.dumps(output_basic_info)
    
@application.route("/keyword/<company>/ratings")
def query(company):
    begin = datetime.datetime(1970,1,1)
    end = datetime.datetime.now()
    page = 0
    dtformat=settings.DATE_FORMAT_KEYWORD
    numperpage = settings.PAGE_SIZE_KEYWORD
    if request.args.get("begin"):
        begin = datetime.datetime.strptime(request.args.get("begin"), dtformat)
    if request.args.get("end"):
        end = datetime.datetime.strptime(request.args.get("end"), dtformat)
    if request.args.get("page"):
        page = int(request.args.get("page"))
    
    sess = db.Session()
    tasks= sess.query(db.Task,db.Keyword,db.Project).filter \
        (db.Keyword.keyword==company, \
        db.Task.project_id==db.Project.id, \
        db.Task.keyword_id==db.Keyword.id,\
        db.Project.datetime.between(begin,end) \
        ).order_by(db.Project.datetime)[page*numperpage: page*numperpage+numperpage]
    outdict = {"ratings":[]}
    for t,k,p in tasks:
        tempdict = { "date":"", "rating":0}
        if t.finished_rating == None:
            continue
        tempdict["date"] = str(p.datetime)
        tempdict["rating"] = t.finished_rating
        outdict["ratings"].append(tempdict);
        
            
    return json.dumps(outdict)

if __name__ == "__main__":
    application.debug = True
    application.run()
