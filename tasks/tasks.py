from celery import Celery
from celery.schedules import crontab

from dbcon.config import REDIS_HOST, REDIS_PASS
from functions import check_docs

app = Celery('tasks', broker=f'redis://:{REDIS_PASS}@{REDIS_HOST}:6379/1')
app.conf.timezone = 'Asia/Yekaterinburg'

app.conf.beat_schedule = {
    'add-every-5-minutes': {
        'task': 'tasks.tasks.start_check_docs',
        'schedule': crontab(minute='*/5'),
    },
}


@app.task
def start_check_docs():
    result = check_docs()
    return result
