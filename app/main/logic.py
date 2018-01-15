#-*- coding:utf-8 -*-
from . import LoginUtils
from . import db_session
from . import User
from . import BaseLogic
import time, hashlib
from flask import current_app, url_for

class LoginLogic(BaseLogic):
    def __init__(self):
        self.session = db_session()
    def signup(self, username, password, *args, **kwargs):
        if  self.is_username_unique(username):
            salt = LoginUtils.get_uuid()
            final_pwd = LoginUtils.hash_str(password + salt)
            create_time = update_time = LoginUtils.get_now_datetime()
            user = User(username=username,
                        nickname='',
                        password=final_pwd,
                        salt=salt,
                        create_time=create_time,
                        update_time=update_time)
            self.session.add(user)
            self.session.commit()
            return {'success': True, 'msg': 'ok'}
        else:
            return {'success': False, 'msg': 'username is exiest'}
            pass
        self.session.close()
        pass
    
    def is_username_unique(self, username):
        c = self.session.query(User).filter(User.username == username).count()
        if c > 0:
            return False
        else:
            return True
        pass

    def get_user_via_name(self, username):
        return self.session.query(User).filter(User.username == username).first()
    
    def login(self, username, password, *args, **kwargs):
        user = self.get_user_via_name(username)
        result = False
        msg = ''
        if user:
            if user.password == LoginUtils.hash_str(password + user.salt):
                result = True
                msg = 'welcome back, %s >.<' % user.nickname
            else:
                result = False
                msg = 'password not correct, please try again T.T'
        else:
            result = False
            msg = 'user not exist @.@'
        return {'success': result, 'msg': msg}

    def logout(self, session):
        session.pop('us', None)
        return {'success': True, 'msg': 'madane'}
        pass