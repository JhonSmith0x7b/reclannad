#-*- coding:utf-8 -*-
from . import catch_vungle
from flask import request, url_for, send_from_directory
from datetime import datetime
import pandas as pd
from .config import DB_PATH 
@catch_vungle.route('/')
def hello():
    return 'hello world'

@catch_vungle.route('/get/<date>/')
def get_vungle_via_date(date='all'):
    try:
        session, engine, Output_table = connect_db()
        query = session.query(Output_table).filter(Output_table.date.like('%{0}%'.format(date))) \
                    if date == 'date' else \
                   session.query(Output_table) 
        df = pd.read_sql(query.statement, engine)
        fname = 'output_%s.csv' % date
        df.to_csv('%s/%s' % (catch_vungle.static_folder, fname), sep=',', index=False)
        return send_from_directory(catch_vungle.static_folder, filename=fname, as_attachment=True)
    except Exception as e:
        print('get vungle err: %s' % str(e))
        return 'sth wrong.'
    pass

def connect_db():
    '''
    db area
    '''
    import sqlalchemy
    from sqlalchemy.ext.declarative import declarative_base 
    from sqlalchemy import create_engine, Column, Integer, Float, String, Boolean
    from sqlalchemy.orm import sessionmaker
    Base = declarative_base()
    engine = create_engine(DB_PATH, echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()
    TEMP_TABLE = 'temp_table'
    OUTPUT_TABLE = 'output_table'
    class Output_table(Base):
        __tablename__ = OUTPUT_TABLE
        id = Column(Integer, primary_key=True)
        application_id  = Column(String)
        application_name = Column(String)
        platform = Column(String)
        country = Column(String)
        date = Column(String)
        datetime = Column(String)
        timestamp = Column(Float)
        clicks = Column(Float)
        completes = Column(Float)
        revenue = Column(Float)
        views = Column(Float)
        is_update = Column(Boolean)
        pre_time = Column(String)
        update_time = Column(String)
        diff_clicks = Column(Float)
        diff_completes = Column(Float)
        diff_revenue = Column(Float)
        diff_views = Column(Float)
    class Temp_table(Base):
        __tablename__ = TEMP_TABLE
        id = Column(Integer, primary_key=True)
        application_id  = Column(String)
        application_name = Column(String)
        platform = Column(String)
        country = Column(String)
        date = Column(String)
        datetime = Column(String)
        timestamp = Column(Float)
        clicks = Column(Float)
        completes = Column(Float)
        revenue = Column(Float)
        views = Column(Float)
        is_update = Column(Boolean)
        pre_time = Column(String)
        update_time = Column(String)
        diff_clicks = Column(Float)
        diff_completes = Column(Float)
        diff_revenue = Column(Float)
        diff_views = Column(Float)
    Base.metadata.create_all(engine)
    def df2db(tablename, df):
        if tablename == 'temp_table':
            def t(row):
                temp = Temp_table()
                temp.application_id = row['application_id']
                temp.application_name = row['application_name']
                temp.platform = row['platform']
                temp.country = row['country']
                temp.date = row['date']
                temp.datetime = row['datetime']
                temp.timestamp = row['timestamp']
                temp.clicks = row['clicks']
                temp.completes = row['completes']
                temp.revenue = row['revenue']
                temp.views = row['views']
                temp.is_update = row['is_update']
                temp.pre_time = row['pre_time']
                temp.update_time = row['update_time']
                temp.diff_clicks = row['diff_clicks']
                temp.diff_completes = row['diff_completes']
                temp.diff_revenue = row['diff_revenue']
                temp.diff_views = row['diff_views']
                session.add(temp)
            df.apply(t, axis=1)
            session.commit()
            pass
        elif tablename == 'output_table':
            def t(row):
                temp = Output_table()
                temp.application_id = row['application_id']
                temp.application_name = row['application_name']
                temp.platform = row['platform']
                temp.country = row['country']
                temp.date = row['date']
                temp.datetime = row['datetime']
                temp.timestamp = row['timestamp']
                temp.clicks = row['clicks']
                temp.completes = row['completes']
                temp.revenue = row['revenue']
                temp.views = row['views']
                temp.is_update = row['is_update']
                temp.pre_time = row['pre_time']
                temp.update_time = row['update_time']
                temp.diff_clicks = row['diff_clicks']
                temp.diff_completes = row['diff_completes']
                temp.diff_revenue = row['diff_revenue']
                temp.diff_views = row['diff_views']
                session.add(temp)
            df.apply(t, axis=1)
            session.commit()
            pass
        pass
    '''
    db end
    ''' 
    return session, engine, Output_table