import sys
sys.path.append('..')
from flask import Blueprint
from ..databases import db_session
from ..models import Article
from ..utils import ArticleUtils
from ..logic import BaseLogic
render_template = ArticleUtils.render_template

article = Blueprint('article', __name__, url_prefix='/article')

from . import views