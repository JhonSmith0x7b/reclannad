import sys
sys.path.append('..')
from ..utils import LoginUtils
render_template = LoginUtils.render_template
from flask import Blueprint
from ..databases import db_session
from .. models import User
from ..logic import BaseLogic

main = Blueprint('main', __name__)

from . import errors, views