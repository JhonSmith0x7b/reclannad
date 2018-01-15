#-*- coding:utf-8 -*-

from flask import Blueprint

tiebasearch = Blueprint('tiebasearch', 
                        __name__,
                        static_folder='static',
                        template_folder='templates',
                        url_prefix='/tiebasearch')

from . import views