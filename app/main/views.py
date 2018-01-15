#-*- coding:utf-8 -*-
from . import main
from flask import redirect, url_for, render_template, request, session
from . import LoginUtils
from .logic import LoginLogic
import json
@main.route('/', methods=['get', 'post'])
def hello():
    return redirect(url_for('novel.hello'))

@main.route('/favicon.ico', methods=['get'])
def favicon():
    return redirect(url_for('static',filename='images/favicon.ico'))

@main.route('/main/login/')
def login():
    return render_template('main/login.htm'), \
            200, \
            LoginUtils.get_content_type()
    pass

@main.route('/main/user/login/', methods=['post'])
def user_login():
    username = request.values.get('username', '')
    session['username'] = username
    password = request.values.get('pwd', '')
    login = LoginLogic()
    result = login.login(username, password)
    if result['success']:
        session['us'] = True
        pass
    else:
        pass
    return json.dumps(result, ensure_ascii=False),\
             200, \
             LoginUtils.get_content_type('text/json')

@main.route('/main/user/signup/', methods=['post'])
def user_signup():
    username = request.values.get('username', '')
    password = request.values.get('pwd', '')
    login = LoginLogic()
    result = login.signup(username, password)
    if result['success']:
        pass
    else:
        pass
    return json.dumps(result, ensure_ascii=False),\
             200, \
             LoginUtils.get_content_type('text/json')

@main.route('/main/user/logout/', methods=['post'])
def user_logout():
    login = LoginLogic()
    result = login.logout(session)
    return json.dumps(result, ensure_ascii=False), \
            200, \
            LoginUtils.get_content_type('text/json')
    pass

@main.route('/main/file/upload/', methods=['post'])
def file_upload():
    logic = LoginLogic()
    upload_type = request.values.get('type', 'article')
    funcnum = request.values.get('CKEditorFuncNum', '')
    result = logic.file_upload(request.files['upload'], upload_type, funcnum)
    return result, \
            200, \
            LoginUtils.get_content_type('text/json')