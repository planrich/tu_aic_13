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
    date = sqlalchemy.Column(sqlalchemy.Date)

    def __init__(self, date):
        self.date = date;

Base.metadata.create_all(engine)

