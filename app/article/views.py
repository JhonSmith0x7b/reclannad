#-*- coding:utf-8 -*-
from . import article
from flask import request, url_for, session
from .logic import ArticleLogic
from . import ArticleUtils
from . import Article
from . import render_template
import json

@article.route('/list/', methods=['get', 'post'])
def get_articles():
    logic = ArticleLogic()
    page = request.values.get('page', '1')
    page_size = request.values.get('page_size', '3')
    try:
        page = int(page) - 1
        page_size = int(page_size)
    except Exception as e:
        page = 0
        page_size = 3
    result = logic.query_page(page=page, page_size=page_size) 
    articles, max_page = result[0], result[1]
    articles = [{'aid': article.id, 'title': article.title, 'brief': article.content[:321]} for article in articles] 
    if request.method in ['get', 'GET']:
        return render_template('article/index.htm', 
                                articles=articles, 
                                max_page=max_page, 
                                page=page + 1, 
                                page_size=page_size), \
               200, \
               {'Conent-Type': 'text/html;charset=utf-8'}
    else:
        return json.dumps(articles, ensure_ascii=False),\
                200, \
                ArticleUtils.get_content_type('text/json')

@article.route('/<aid>/get/', methods=['get'])
def get_article(aid):
    logic = ArticleLogic()
    article = logic.query(aid)
    if article:
        return render_template('article/page.htm', 
                    article=article), \
               200, \
               ArticleUtils.get_content_type()
    else:
        return 'have not found article T.T'

@article.route('/posted/', methods=['get'])
def posted():
    return render_template('article/posted.htm'), \
           200, \
           ArticleUtils.get_content_type()

@article.route('/post/', methods=['post'])
def article_post():
    title = request.values.get('title', '')
    author = request.values.get('author', '')
    summary = request.values.get('summary', '')
    content = request.values.get('content', '')
    aid = request.values.get('aid', '')
    logic = ArticleLogic()
    if aid == '':
        result = logic.insert(title=title, author=author, content=content, c=summary)
        return json.dumps(result, ensure_ascii=False), \
            200, \
            ArticleUtils.get_content_type('text/json')
    else:
        result = logic.update(id=aid, title=title, author=author, content=content, c=summary)
        return json.dumps(result, ensure_ascii=False), \
            200, \
            ArticleUtils.get_content_type('text/json')
        pass

@article.route('/<aid>/del/', methods=['post'])
def article_del(aid):
    logic = ArticleLogic()
    result = logic.delete(aid)
    return json.dumps(result, ensure_ascii=False), \
           200, \
           ArticleUtils.get_content_type('text/json')

@article.route('/<aid>/edit/', methods=['get'])
def article_edit(aid):
    logic = ArticleLogic()
    article = logic.query(aid) 
    return render_template('article/posted.htm', article=article), \
           200, \
            ArticleUtils.get_content_type()

@article.route('/most_read/get/', methods=['post'])
def most_read_get():
    logic = ArticleLogic()
    articles = logic.query_most()
    articles = {
        'success': True,
        'data': [{'title': article.title, 
                    'aid': article.id}  for article in articles]
    }
    return json.dumps(articles, ensure_ascii=False), \
           200, \
           ArticleUtils.get_content_type('text/json')

@article.route('/recently/get/', methods=['post'])
def recently_get():
    logic = ArticleLogic()
    articles = logic.query_recently()
    articles = {
        'success': True,
        'data': [{
            'title': article.title,
            'aid': article.id
        } for article in articles]
    }
    return json.dumps(articles, ensure_ascii=False), \
            200, \
            ArticleUtils.get_content_type('text/json')