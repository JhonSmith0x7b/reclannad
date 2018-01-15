#-*- coding:utf-8 -*-

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from . import config
engin = create_engine(config['development'].SQLALCHEMY_DATABASE_URI, convert_unicode=True)
Base = declarative_base()
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=True,
                                         bind=engin))
from . import models

def init_db(app):
    Base.metadata.create_all(bind=engin)
