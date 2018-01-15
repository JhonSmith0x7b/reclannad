#-*- coding:utf-8 -*-

from .databases import Base
from sqlalchemy import Column, Integer, String

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    nickname = Column(String)
    password = Column(String)
    salt = Column(String)
    create_time = Column(String)
    update_time = Column(String)
    c = Column(String)
    c1 = Column(String)
    c2 = Column(String)
    c3 = Column(String)
    c4 = Column(String)

class Article(Base):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    content = Column(String)
    create_time = Column(String)
    update_time = Column(String)
    c = Column(String)
    c1 = Column(String)
    c2 = Column(String)
    c3 = Column(String)
    c4 = Column(String) 

