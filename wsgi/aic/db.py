import sqlalchemy
import sqlalchemy.ext.declarative
import sqlalchemy.orm
import settings
from sqlalchemy import Table, Column, Integer, ForeignKey, String, DateTime, Boolean
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
import datetime as dt

engine = sqlalchemy.create_engine(settings.DB_URL)

Session = sqlalchemy.orm.sessionmaker(bind=engine)
Base = sqlalchemy.ext.declarative.declarative_base()

class Publication(Base):
    __tablename__ = 'publications'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    datetime = sqlalchemy.Column(sqlalchemy.DateTime)

    def __init__(self, datetime):
        self.datetime = datetime;

class Keyword(Base):
    __tablename__ = 'keywords'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    keyword = sqlalchemy.Column(sqlalchemy.String)
    tasks = relationship("Task")

    def __init__(self, keyword):
        self.keyword = keyword

class Project(Base):
    __tablename__ = 'projects'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    link = Column(sqlalchemy.String)
    datetime = sqlalchemy.Column(sqlalchemy.DateTime)
    paragraph = sqlalchemy.Column(sqlalchemy.String)

    tasks = relationship("Task")


    def __init__(self, paragraph, link, datetime=dt.datetime.now()):
        self.link = link
        self.paragraph = paragraph
        self.datetime = datetime

class Answer(Base):
    __tablename__ = 'answers'
    id = Column(sqlalchemy.Integer, primary_key=True)
    datetime = Column(sqlalchemy.DateTime)
    value = Column(sqlalchemy.String)
    task_id = Column(sqlalchemy.Integer, ForeignKey('tasks.id'))
    worker_id = Column(sqlalchemy.String, ForeignKey('workers.id'))

    def __init__(self, task, worker, value, datetime=dt.datetime.now()):
        self.task_id = task.id
        self.worker_id = worker.id
        self.datetime = datetime
        self.value = value

    def as_dict(self):
        return {
            'id': self.id,
            'task_id': self.task_id,
            'worker_id': self.worker_id,
            'datetime': self.datetime,
            'value': self.value
        }

class Worker(Base):
    __tablename__ = 'workers'
    id = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    answers = relationship("Answer")

    def __init__(self, worker_id):
        """ provide the workerid from the mobile works system.
            it is assumed it is a string """
        self.id = worker_id


class Task(Base):
    __tablename__ = 'tasks'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    paragraph =  Column(sqlalchemy.String)
    project_id = Column(sqlalchemy.Integer, ForeignKey('projects.id'))
    keyword_id = Column(sqlalchemy.Integer, ForeignKey('keywords.id'))
    finished_rating = sqlalchemy.Column(sqlalchemy.Integer)
    answers_requested = Column(Integer)
    price = Column(sqlalchemy.Float)
    price_factor = Column(sqlalchemy.Float)

    answers = relationship("Answer")

    def __init__(self, project, keyword, paragraph):
        self.project_id = project.id
        self.keyword_id = keyword.id
        self.paragraph = paragraph
        self.finished_rating = None
        self.price = 0.02
        self.price_factor = 1

    def calculate_rating(self):
        negative = 0
        positive = 0
        neutral = 0
        for answer in self.answers:
            if answer.value == 'negative':
                negative += 1
            elif answer.value == 'positive':
                positive += 1
            else:
                neutral += 1
        if positive > negative and positive > neutral:
            self.finished_rating = 10
        elif negative > positive and negative > neutral:
            self.finished_rating = 0
        else:
            self.finished_rating = 5


Base.metadata.create_all(engine)

