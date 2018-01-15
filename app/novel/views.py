#-*- coding:utf-8 -*-

from . import novel
from flask import request, render_template, url_for, current_app
import json


@novel.route('/index/', methods=['get'])
def hello():
    action = request.args.get('action', '')
    chapter = request.args.get('chapter', '')
    if action != '' and chapter != '':
        if action == 'readnovel':
            content = Novel_reader(chapter).read()
            return render_template('main.htm', action='readnovel', content=content), \
                200, {'Content-Type': 'text/html;charset=utf-8'}
    return render_template('main.htm'), \
            200, {'Content-Type': 'text/html;charset=utf-8'}


class Novel_reader:
    def __init__(self, chapter='fuuko'):
        self.f = open(('%s/novel/static/txt/%s.txt') % (current_app.root_path, chapter), 'r')
        pass

    def novel2array(self):
        novel_array = []
        page = ''
        line_counter = 300
        while True:
            current_line = self.f.readline()
            if current_line != '':
                if line_counter > 0:
                    page += (current_line + '<br>')
                    line_counter -= 1
                else:
                    novel_array.append(page)
                    page = (current_line + '<br>')
                    line_counter = 300
            else:
                novel_array.append(page)
                break
        return json.dumps(novel_array, ensure_ascii = False)
        pass

    def read(self):
        return self.novel2array()
        pass