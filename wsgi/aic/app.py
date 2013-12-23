# encoding: utf-8
from flask import Flask, request, render_template, flash, redirect, url_for
from flask.json import jsonify
from sqlalchemy import func

from random import randint
import json

import db
import settings
import utils
import time



application = Flask(__name__)
application.secret_key = settings.SECRET_KEY


# WEBAPP
###########################################################

@application.route('/', methods=['GET'])
def get_index():
    session = db.Session()
    num_keywords = session.query(db.Keyword).count()
    num_resolved_tasks = session.query(db.Task).filter(db.Task.finished_rating != None).count()
    return render_template('index.html', num_keywords=num_keywords, num_resolved_tasks=num_resolved_tasks)

@application.route('/search', methods=['GET'])
def get_search():
    session = db.Session()
    q = request.args.get('q', '')
    result = session.query(db.Keyword).filter(func.lower(db.Keyword.keyword) == func.lower(q)).first()
    if not result:
        return render_template('search.html', q=q)
    return redirect(url_for('get_keyword', k=result.keyword))

@application.route('/keywords/<k>', methods=['GET'])
def get_keyword(k):
    session = db.Session()
    keyword = session.query(db.Keyword).filter(func.lower(db.Keyword.keyword) == func.lower(k)).first()
    if not keyword:
        return redirect(url_for('get_index'))

    # TEST DATA
    mentions = {"positive": [], "neutral": [], "negative": []};
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    for month in months:
        mentions["positive"].append([month, randint(0, 30)])
        mentions["negative"].append([month, randint(0, 30)])
        mentions["neutral"].append([month, randint(0, 30)])

    return render_template('keyword.html', keyword=keyword, mentions=json.dumps(mentions))

@application.route('/admin', methods=['GET'])
def get_admin():
    return redirect(url_for('get_admin_tasks'))

@application.route('/admin/tasks', methods=['GET'])
def get_admin_tasks():
    return render_template('admin.tasks.html')

@application.route('/admin/workers', methods=['GET'])
def get_admin_workers():
    return render_template('admin.workers.html')

@application.route('/admin/keywords', methods=['GET'])
def get_admin_keywords():
    session = db.Session()
    keywords = session.query(db.Keyword).all()
    return render_template('admin.keywords.html', keywords=keywords)

@application.route('/admin/keywords', methods=['POST'])
def post_admin_keywords():
    session = db.Session()
    if request.form['keyword']:
        keyword = db.Keyword(request.form['keyword'])
        session.add(keyword)
        session.commit()
        flash("Keyword created correctly", "success")
    else:
        flash("The keyword can not be empty", "danger")
    return redirect(url_for('get_admin_keywords'))

# API
###########################################################

@application.route("/api/tasks/<task_id>/answers", methods=['POST'])
def post_task_answer(task_id):
    #http://main-tuaic13.rhcloud.com/api/tasks/157/answers
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


@application.route('/query/<company>', defaults={'days': 20})
@application.route("/query/<company>/<int:days>")
def query(company, days):
    sess = db.Session()
    took_me_ms = int(round(time.time() * 1000))
    results = sess.query("rating").from_statement("""
        select avg(t.finished_rating) as rating
        from tasks t, keywords k, projects p
        where
            t.finished_rating is not null and
            t.keyword_id = k.id and
            k.keyword like :keyword and
            t.project_id = p.id and
            (now() - (cast (p.datetime as timestamp))) < interval ':days days'
    """).params(keyword=company, days=days).all()
    took_me_ms = int(round(time.time() * 1000)) - took_me_ms

    if len(results) == 1 and len(results[0]) == 1:
        rating = results[0][0] # first index access returns tuple -> then first
        if rating == None:
            return jsonify(message=\
                """Sorry. No sentiment information is stored \
for %s. Either you mistyped the company or yahoo finance does not \
contain articles about the compnay/product!""" % company)
        rating = format(rating, '.2f')

        details = {
                "message": "The average sentiment of {0} is '{1}'.".format(company, rating),
                "rating":rating,
                "keyword":company,
                "interval":"[0..10]. towards 0 corresponds to negative, whereas 10 is positive",
                "timespan":"the last %d day(s)" % days
                }
        if request.args.get('d') is not None:
            details['ms'] = took_me_ms
        return jsonify(**details)
    else:
        return jsonify(message=\
                """Sorry. No sentiment information is stored \
for %s. Either you mistyped the company or yahoo finance does not \
contain articles about the compnay/product!""" % company)

    #tasks = sess.query(db.Keyword, db.Task).filter \
    #    (db.Keyword.keyword==company \
    #    # and db.Project.finishedRating != None \  does not work
    #    and db.projects.datetime > date.today - timespan)
    #cnt=0
    #total=0
    #for k,t in tasks:
    #    if k.finishedRating == None:
    #        continue
    #    cnt+=1
    #    total+=int(p.finished_rating or 0)
    #    #out += str(total)
    #if cnt == 0:
    #    return '{}'
    #return '{"'+company+ '":' + str(1.0*total/cnt) + '}'

if __name__ == "__main__":
    application.debug = True
    application.run()
