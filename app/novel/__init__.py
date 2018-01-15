#-*- coding:utf-8 -*-

from flask import Blueprint

novel = Blueprint('novel', 
                    __name__, 
                    static_folder='static', 
                    template_folder='templates',
                    url_prefix='/novel'
                    )

from . import views