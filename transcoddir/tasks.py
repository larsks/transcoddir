from __future__ import absolute_import

import logging
from pathlib2 import Path

from celery import Celery
from . import engine
from . import celeryconfig

LOG = logging.getLogger(__name__)

app = Celery('transcode', broker=celeryconfig.BROKER_URL)
app.config_from_object(celeryconfig)


@app.task
def process_torrent(torrent, profile='ipad', keep=False):
    e = engine.Engine(profile=profile, keep=keep)
    path = Path(torrent['torrent_dir']) / torrent['torrent_name']
    e.process(path)
