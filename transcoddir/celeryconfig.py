import os

BROKER_URL = os.environ.get('CELERY_BROKER_URL')

CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_QUEUES = {
    'default': dict(exchange='celery', routing_key='celery'),
    'video': dict(exchange='video', routing_key='video')
}
CELERY_DEFAULT_QUEUE = 'default'

CELERY_ROUTES = {
    'transcoddir.tasks.process_torrent': 'video',
}
