from __future__ import absolute_import

import os
from . import tasks


def torrent_done():
    torrent = {}
    for k, v in os.environ.items():
        if k.startswith('TR_'):
            torrent[k[3:].lower()] = v

    for required in ['torrent_dir', 'torrent_name']:
        if required not in torrent:
            raise KeyError('missing required environment variables')

    tasks.process_torrent.delay(torrent)
