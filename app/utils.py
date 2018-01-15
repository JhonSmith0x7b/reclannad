#-*- coding:utf-8 -*-

class BaseUtils(object):
    def __init__(self):
        pass
    @staticmethod
    def get_now_datetime(strf='%Y-%m-%d %H:%M:%S'):
        from datetime import datetime
        return datetime.now().strftime(strf)

    @staticmethod
    def get_uuid():
        import uuid
        return str(uuid.uuid4())    
    
    @staticmethod
    def hash_str(s):
        import hashlib
        return hashlib.sha256(s if type(s) is bytes else s.encode('utf-8')).hexdigest()

    @staticmethod
    def check_login():
        from flask import session
        if 'us' in session:
            return True
        else:
            return False
        pass

    @staticmethod
    def render_template(*args, **kwargs):
        from flask import render_template
        return render_template(*args, **kwargs, check_login=BaseUtils.check_login)

    @staticmethod
    def get_content_type(typical='text/html', encode='utf-8'):
        return {'Content-Type': '%s;charset=%s' % (typical, encode)}
        pass

class LoginUtils(BaseUtils): 
    pass

class ArticleUtils(BaseUtils):
    pass