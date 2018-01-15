#-*- coding:utf-8 -*-

from flask import render_template, current_app, request, g
from . import tiebasearch
import sqlite3, json
from datetime import datetime

@tiebasearch.route('/', methods=['get'])
def tieba_search():
    return render_template('tiebasearch.htm'), \
            200, {'Content-Type': 'text/html;charset=utf-8'}
    pass

@tiebasearch.route('/r/', methods=['post'])
def r():
    who = request.form.get('who', '')
    if(who != ''):
        _datetime = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
        R().r(who, request.remote_addr, _datetime)
    return 's', 200, {'Content-Type':'text/plain;charset=utf-8'}
    pass
@tiebasearch.route('/query/', methods=['post'])
def query():
    if(request.form['date'] == 'all'):
        cur = get_tieba_db().cursor().execute('select * from tiebadata_table where author = ?', (request.form['author'], ))
    else:
        cur = get_tieba_db().cursor().execute('select * from tiebadata_table where author = ? and datetime(date) > ? and datetime(date) < ?', (request.form['author'], request.form['date'], str(int(request.form['date']) + 1)))
    result = cur.fetchall()
    return json.dumps(result, ensure_ascii=False), 200, {'Content-Type':'text/json;charset=utf-8'}
    pass

@tiebasearch.route('/jhonsmithsbackdoor/', methods=['get'])
def backdoor():
    db_path = '%s/tiebasearch/static/db/tiebarecord_db.db' % current_app.root_path
    cursor = sqlite3.connect(db_path).cursor()
    sql = """
    select * from r
    """
    result = cursor.execute(sql).fetchall()
    return render_template('backdoor.htm', data=json.dumps(result)),
    200, {'Content-Type':'text/html;charset=gbk'}
    pass

def get_tieba_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('%s/tiebasearch/static/db/new_tiebadata_db.db' % current_app.root_path)
    return db



class R():
    def __init__(self):
        db_path = '%s/tiebasearch/static/db/tiebarecord_db.db' % current_app.root_path
        self.db = sqlite3.connect(db_path)
        self.check_table()
        pass
    def check_table(self):
        try:
            sql = 'select count(*) from r'
            cursor = self.db.cursor()
            cursor.execute(sql)
            result = cursor.fetchall()
            if result[0] != None:
                return
        except Exception as e:
            sql = 'create table r(date text, ip text, author text)'
            cursor = self.db.cursor()
            cursor.execute(sql)
            self.db.commit()
    def r(self, who, ip, datetime):
        sql = """
        insert into r(date, ip, author) values(?, ?, ?)
        """
        cursor = self.db.cursor()
        cursor.execute(sql, (who, ip, datetime))
        self.db.commit()
        pass