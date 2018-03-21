#-*- coding:utf-8 -*-
from celery import Celery
from . import celery_config
import requests, json, asyncio, redis
from datetime import datetime
from . import config

#celery -A app.drrr.tasks worker  --loglevel=info
celery = Celery('tasks')
celery.config_from_object(celery_config)

@celery.task
def convence_album(album):
    album_title, songs = album['title'], album['songs']
    # loop = asyncio.get_event_loop()
    # results = []
    # async def get_url(song):
    #     id = song['id']
    #     title = song['title']
    #     get = lambda:requests.get(f'http://music.163.com/song/media/outer/url?id={id}')
    #     resp = await loop.run_in_executor(None, get)
    #     if 'mp3' in resp.url:
    #         url = resp.url
    #         results.append({
    #             'id': id,
    #             'title': title,
    #             'url': url
    #         })
    # loop.run_until_complete(asyncio.gather(*[get_url(song) for song in songs]))
    # print(results)
    sediment_album({
        'title': album_title,
        'songs': songs
    })

def sediment_album(album):
    r = redis.StrictRedis(host=config.REDIS_HOST, 
                            port=config.REDIS_PORT, 
                            db=config.REDIS_DRRR_DB)
    title, songs = f'{album["title"]}?{datetime.strftime(datetime.now(), "%Y%m%d-%H:%M:%S")}', album['songs']
    for song in songs:
        r.sadd(title, json.dumps(song, ensure_ascii=False))