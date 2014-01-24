# encoding: utf-8
from flask import Flask, request, render_template, flash, redirect, url_for
from flask.json import jsonify
from flask.ext.paginate import Pagination
from sqlalchemy import func

from random import randint
import json
import operator
import datetime as dt

import db
import settings
import utils
import time
import ago

import argparse


application = Flask(__name__)
application.secret_key = settings.SECRET_KEY

# schedules jobs
from apscheduler.scheduler import Scheduler
from scraper import scrape
from dynamic_pricer import dynamic_pricing
from garbage_collector import garbage_collecting


# Filters for templates
application.jinja_env.filters['humanize_date'] = utils.humanize_date
application.jinja_env.filters['rate_average'] = utils.rate_average
application.jinja_env.filters['ago'] = ago.human

# Logging
import logging
logger = settings.createLog("main_app")


# WEBAPP
###########################################################

@application.route('/', methods=['GET'])
def get_index():
    with db.session_scope() as session:
        num_keywords = session.query(db.Keyword).count()
        num_resolved_tasks = session.query(db.Task).filter(db.Task.finished_rating != None).count()
        return render_template('index.html',
                    num_keywords=num_keywords,
                    num_resolved_tasks=num_resolved_tasks)

@application.route('/search', methods=['GET'])
def get_search():
    with db.session_scope() as session:
        q = request.args.get('q', '')
        keyword = session.query(db.Keyword).filter(func.lower(db.Keyword.keyword) == func.lower(q)).first()
        if not keyword:
            return render_template('search.html', q=q)
        if keyword.num_mentions(session) == 0:
            return render_template('search.html', q=q)
        return redirect(url_for('get_keyword', k=keyword.keyword))

@application.route('/keywords/<k>', methods=['GET'])
def get_keyword(k):
    with db.session_scope() as session:
        keyword = session.query(db.Keyword).filter(func.lower(db.Keyword.keyword) == func.lower(k)).first()
        if not keyword:
            return redirect(url_for('get_index'))

        num_mentions = keyword.num_mentions(session)
        if num_mentions == 0:
            return render_template('search.html', q=q)

        average = keyword.average_rating(session)
        mentions = keyword.last_year_mentions(session)

        return render_template('keyword.html', keyword=keyword,
                               average=average, mentions=json.dumps(mentions),
                               num_mentions=num_mentions)

@application.route('/admin', methods=['GET'])
def get_admin():
    return redirect(url_for('get_admin_tasks'))

@application.route('/admin/tasks', methods=['GET'])
def get_admin_tasks():
    with db.session_scope() as session:
        try:
            page = int(request.args.get('page', 1))
        except ValueError:
            page = 1
        per_page = 10
        task_count = session.query(db.Task)\
                .filter(db.Task.finished_rating == None).count()
        tasks = session.query(db.Task)\
                .filter(db.Task.finished_rating == None)\
                .order_by(db.Task.datetime)\
                .limit(per_page)\
                .offset((page-1)*per_page).all()
        for task in tasks:
            task.keyword = session.query(db.Keyword).filter(db.Keyword.id == task.keyword_id).first().keyword
            task.answered = session.query(db.Answer).filter(db.Answer.task_id == task.id).count()
        pagination = Pagination(page=page,
                total=task_count,
                search=False,
                per_page=per_page,
                bs_version=3)
        return render_template('admin.tasks.html',
                tasks=tasks,
                pagination=pagination)

@application.route('/admin/workers', methods=['GET'])
def get_admin_workers():
    with db.session_scope() as session:
        workers = session.query(db.Worker).order_by(db.Worker.worker_rating, db.Worker.id).all()
        return render_template('admin.workers.html', workers = workers)

@application.route("/admin/workers", methods=['POST'])
def post_worker_toggle():
    with db.session_scope() as session:
        if not request.form["worker_id"]:
             flash("Worker not found", "fail")
             return redirect(url_for('get_admin_workers'))

        worker_id = request.form["worker_id"]
        worker = session.query(db.Worker).filter(db.Worker.id==worker_id).first()

        if not worker:
            flash("Worker not found", "fail")
        else:
            if worker.blocked==1:
                worker.blocked=0
            else:
                worker.blocked=1
            session.commit()
        return redirect(url_for('get_admin_workers'))

@application.route('/admin/keywords', methods=['GET'])
def get_admin_keywords():
    with db.session_scope() as session:
        keywords = session.query(db.Keyword).all()

        ratings = {}
        ranks = {}
        rank = 1
        for kw_obj in keywords:
            keyword = kw_obj.keyword
            rating = calc_avg_sentiment(session, keyword, 20)
            if rating is not None:
                ratings[keyword] = "{0:.2f}".format(rating)
            else:
                ratings[keyword] = "None"

        sorted_ratings = sorted(ratings.iteritems(), key=operator.itemgetter(1))
        rank = 1
        for keyword, _ in sorted_ratings:
            ranks[keyword] = rank
            rank += 1

        return render_template('admin.keywords.html',
                keywords=keywords,
                ratings=ratings,
                ranks=ranks)

@application.route('/admin/keywords', methods=['POST'])
def post_admin_keywords():
    with db.session_scope() as session:
        if request.form['keyword']:
            keyword = db.Keyword(request.form['keyword'])
            keyword.added = dt.datetime.now()
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
    with db.session_scope() as session:
        task = session.query(db.Task).filter(db.Task.id == task_id).first()
        if not task:
            return jsonify(error='Task not found'), 404

        raw_answer = utils.get_raw_answer(request)
        if not raw_answer:
            return jsonify(error='Error parsing json'), 400

        worker_id = raw_answer['user']
        worker = session.query(db.Worker).filter(db.Worker.id == worker_id).first()
        if not worker:
            worker = db.Worker(worker_id, 0, 0)
            session.add(worker)
            session.commit()

        if worker.blocked == 1:
            return jsonify(error='Unfortunately, your account has been blocked'), 401

        answer = db.Answer(task, worker, raw_answer['answer'])
        session.add(answer)
        session.commit()

        if len(task.answers) == task.answers_requested:
            task.calculate_rating()

            session.add(task)
            session.commit()
            task.rate_workers()
            session.commit()

        return jsonify(answer.as_dict()), 200

def calc_avg_sentiment(session, company, days = 20):
    results = session.query("rating").from_statement("""
        select avg(t.finished_rating) as rating
        from tasks t, keywords k, projects p
        where
            t.finished_rating is not null and
            t.keyword_id = k.id and
            k.keyword ilike :keyword and
            t.project_id = p.id and
            (now() - (cast (p.datetime as timestamp))) < interval ':days days'
    """).params(keyword=company, days=days).all()
    avg_row = results[0]
    if len(avg_row) == 1:
        return avg_row[0]
    else:
        return None

@application.route('/query/<company>', defaults={'days': 20})
@application.route("/query/<company>/<int:days>")
def query(company, days):
    with db.session_scope() as session:
        took_me_ms = int(round(time.time() * 1000))
        result = calc_avg_sentiment(session, company, days)
        took_me_ms = int(round(time.time() * 1000)) - took_me_ms

        if result is not None:
            rating = result
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

def startScheduledJobs():
    logger.info("startScheduledJobs")
    sc = Scheduler()
    sc.start()
    # Schedule  to be called every hour
    sc.add_interval_job(scrape, minutes=1)
    sc.add_interval_job(dynamic_pricing, hours=1)
    sc.add_interval_job(garbage_collecting, hours=1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--demo", help="run in demo mode, without scheduled tasks", action="store_true")
    args = parser.parse_args()
    if not args.demo:
        startScheduledJobs()
    else:
        logger.info()

    application.debug = True
    application.run()


