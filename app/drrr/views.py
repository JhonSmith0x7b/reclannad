#-*- coding:utf-8 -*-
from . import drrr
from flask import request
import json, requests, redis
from .tasks import convence_album
import pandas as pd
from pandas import DataFrame, Series
from . import config
@drrr.route('/')
def hello():
    return 'hello drrr'

@drrr.route('/album/dummy/', methods=['get'])
def album_post():
    album = request.args.get('album', '')
    result = ''
    if album:
        result = 'succ'
        convence_album.delay(json.loads(album))
    callback = request.args.get('callback', '')
    return f'{callback}("succ")', 200, \
            {'Content-Type': 'text/plain;charset=utf-8'}

@drrr.route('/song/convence/', methods=['get'])
def convence():
    id = request.args.get('id', '')
    url = 'get failed.'
    callback = request.args.get('callback', '')
    if id:
        resp = requests.get(f'http://music.163.com/song/media/outer/url?id={id}')
        if '.mp3' in resp.url:
            url = resp.url
    return f'{callback}("{url}")', 200, \
            {'Content-Type': 'text/plain;charset=utf-8'}

@drrr.route('/album/', methods=['get'])
def get_album():
    key = request.args.get('key', '')
    key = requests.utils.unquote(key)
    r = redis.StrictRedis(host=config.REDIS_HOST, 
                            port=config.REDIS_PORT, 
                            db=config.REDIS_DRRR_DB)
    results = None
    if key:
        results = []
        temp = r.smembers(key)
        for result in temp:
            result = json.loads(result.decode())
            results.append(result)
    else:
        results = r.keys()
    callback = request.args.get('callback', '')
    if callback:
        data = json.dumps(results, cls=MyEncoder, ensure_ascii=False)
        return f'{callback}(\'{requests.utils.quote(data)}\')', 200, \
                {'Content-Type': 'text/plain;charset=utf-8'}
    return json.dumps(results, cls=MyEncoder, ensure_ascii=False), 200, \
            {'Content-Type': 'text/json;charset=utf-8'}

class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        # pylint: disable=E0202
        if isinstance(obj, (bytes, bytearray)):
            return obj.decode('utf-8')
        return json.JSONEncoder.default(self, obj)
    

    