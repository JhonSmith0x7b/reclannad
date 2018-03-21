#-*- coding:utf-8 -*-
from flask import Blueprint
import sys
sys.path.append('..')
drrr = Blueprint('drrr',
                    __name__,
                    static_folder='static',
                    template_folder='templates',
                    url_prefix='/drrr')
from . import views