#-*- coding:utf-8 -*-
from . import app
from .databases import db_session
@app.errorhandler(404)
def page_not_found(e):
    return '404', 404

@app.errorhandler(500)
def internal_server_error(e):
    return '500', 500

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
    pass    