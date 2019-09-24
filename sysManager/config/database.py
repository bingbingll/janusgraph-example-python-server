from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


class pgsql:
    engine = create_engine('postgresql://postgres:postgres@172.16.2.107:5432/jg_sys', client_encoding='utf8',
                           echo=True,
                           convert_unicode=True,
                           pool_size=30,
                           pool_recycle=1800)

    db_session = scoped_session(sessionmaker(autocommit=False,
                                             autoflush=False,
                                             bind=engine))
    Base = declarative_base()
    Base.query = db_session.query_property()


def init_db():
    pgsql.Base.metadata.create_all(bind=pgsql.engine)
