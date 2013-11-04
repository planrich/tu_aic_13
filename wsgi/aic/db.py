import sqlalchemy
import sqlalchemy.ext.declarative
import sqlalchemy.orm
import settings
from sqlalchemy import Table, Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
import datetime as dt

engine = sqlalchemy.create_engine(settings.DB_URL)

Session = sqlalchemy.orm.sessionmaker(bind=engine)
Base = sqlalchemy.ext.declarative.declarative_base()

class OpenTask(Base):
    __tablename__ = 'open_tasks'
    id = Column(String, primary_key=True)
    datetime = Column(DateTime)
    task_description = Column(String)
    answer_possibility = Column(String) # hacky
    price_cents = Column(Integer)
    callback_link = Column(String)

    def __init__(self, id, desc, answer, link, cents):
        self.id = id
        self.task_description = desc
        self.answer_possibility = answer
        self.callback_link = link
        self.price_cents = cents
        self.datetime = dt.datetime.now()


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
    finishedRating = sqlalchemy.Column(sqlalchemy.Integer)

    tasks = relationship("Task")


    def __init__(self, paragraph, link,\
            finishedRating = None,\
            datetime=dt.datetime.now()):
        self.link = link
        self.paragraph = paragraph
        self.datetime = datetime
        self.finishedRating = finishedRating

class Answer(Base):
    __tablename__ = 'answers'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    datetime = sqlalchemy.Column(sqlalchemy.DateTime)
    rating = sqlalchemy.Column(sqlalchemy.Integer)
    task_id = Column(sqlalchemy.Integer, ForeignKey('tasks.id'))
    worker_id = Column(sqlalchemy.String, ForeignKey('workers.id'))

    def __init__(self, task, worker, rating, datetime=dt.datetime.now()):
        self.taks_id = task.id
        self.worker_id = worker.id
        self.datetime = datetime
        self.rating = rating

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
    answers = relationship("Answer")

    def __init__(self, project, keyword, paragraph):
        self.project_id = project.id
        self.keyword = keyword
        self.paragraph = paragraph


Base.metadata.create_all(engine)

