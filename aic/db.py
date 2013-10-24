import sqlalchemy
import sqlalchemy.ext.declarative
import sqlalchemy.orm
import settings

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

    def __init__(self, keyword):
        self.keyword = keyword

class Task(Base):
    __tablename__ = 'tables'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    paragraph = sqlalchemy.Column(sqlalchemy.String)

    def __init__(self, keyword):
        self.keyword = keyword


Base.metadata.create_all(engine)

