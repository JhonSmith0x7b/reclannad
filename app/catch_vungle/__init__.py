#-*- coding:utf-8 -*-
from flask import Blueprint
catch_vungle = Blueprint('catch_vungle',
                            __name__,
                            static_folder='static',
                            template_folder='templates',
                            url_prefix='/catch_vungle')
from . import views