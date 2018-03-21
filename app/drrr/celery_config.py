#-*- coding:utf-8 -*-
from . import config
broker_url = f'redis://{config.REDIS_HOST}/{config.REDIS_BORKER_DB}'
result_backend = 'rpc://'
task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
#timezone = 'Europe/Oslo'
enable_utc = True
task_routes = {
    'app.drrr.tasks worker': 'low-priority',
}