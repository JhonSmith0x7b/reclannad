#-*- coding:utf-8 -*-
from . import ArticleUtils
from . import db_session
from . import Article
from . import BaseLogic
from io import StringIO, BytesIO
import math, re, requests

class ArticleLogic(BaseLogic):
    def __init__(self):
        self.session = db_session()
        pass

    def insert(self, **kwargs):
        article = Article(**kwargs)
        if article.content:
            article.content = self.modify_content(article.content)
        article.create_time = article.update_time = ArticleUtils.get_now_datetime()
        self.session.add(article)
        self.session.commit()
        self.session.flush()
        self.session.refresh(article)
        return {'success': True, 'aid': article.id}
        pass        
    
    def update(self, **kwargs):
        article = self.session.query(Article).filter(Article.id==kwargs['id']).first()
        article.title = kwargs['title']
        article.author = kwargs['author']
        article.content = kwargs['content']
        article.c = kwargs['c']
        article.update_time = ArticleUtils.get_now_datetime()
        self.session.commit()
        return {'success': True, 'aid': article.id}
        

    def modify_content(self, content):
        replace_results = re.findall(r'<img.*?src="(.*?)".*?/>', content)
        for _ in replace_results:
            if _[:4] == 'http':
                resp = requests.get(_)
                if resp.status_code == 200:
                    if 'Content-Type' in resp.headers.keys():
                        bio = BytesIO(resp.content)
                        bio.mimetype = resp.headers['Content-Type']
                        bio.filename = _.split('/')[-1]
                        img_url = self.file_upload(bio, 'modify_content')
                        content = content.replace(_, img_url)
        return content
        pass
     
    def query(self, aid=None):
        if aid:
            article = self.session.query(Article).filter(Article.id==aid).first()
            if not article.c1:
                article.c1 = 0
            article.c1 = int(article.c1) + 1
            self.session.commit()
            article.content = self.decorate_content(article.content)
            return article
        else:
            articles = self.session.query(Article)[:10]
            return articles
        pass

    def query_page(self, page=0, page_size=3):
        page, page_size = int(page), int(page_size)
        articles = self.session.query(Article)[page * page_size: page * page_size + page_size]
        article_num = self.session.query(Article).count()
        max_page = math.ceil(article_num / page_size)
        return articles, max_page 
        pass
    
    def query_most(self):
        articles = self.session.query(Article).order_by(Article.c1.desc())[:5]
        return articles
    
    def query_recently(self):
        articles = self.session.query(Article).order_by(Article.update_time.desc())[:5]
        return articles

    def decorate_content(self, content):
        if '<p>' in content:
            return content
        d_content = '<p>'
        content = StringIO(content)
        while True:
            temp = content.read(1)
            if len(temp) > 0:
                if temp in ['\n']:
                    d_content += '</p><p>'
                else:
                    d_content += temp
            else:
                break
        return d_content + '</p>'
        pass

    def delete(self, aid):
        article = self.session.query(Article).filter_by(id=aid).first()
        self.session.delete(article)
        self.session.commit()
        return {
                'success': True
                }
    