#-*- coding:utf-8 -*-
from flask import Flask
import sys
sys.path.append('..')
from config import config
app = Flask(__name__)
from . import handlers
from .main import main
app.register_blueprint(main)
from .article import article
app.register_blueprint(article)
from .novel import novel
app.register_blueprint(novel)
from .databases import init_db
from .tiebasearch import tiebasearch
app.register_blueprint(tiebasearch)
from .catch_vungle import catch_vungle
app.register_blueprint(catch_vungle)
from .drrr import drrr
app.register_blueprint(drrr)
init_db(app)
app.debug = config['development'].DEBUG
app.secret_key = config['development'].APP_SECRET
