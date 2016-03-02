#!/usr/bin/python

from __future__ import absolute_import

import argparse
import yaml
import logging
import pkg_resources
from pathlib2 import Path

from . import tasks

LOG = logging.getLogger(__name__)

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('--verbose', '-v',
                   action='store_const',
                   const='INFO',
                   dest='loglevel')
    p.add_argument('--debug', '-d',
                   action='store_const',
                   const='DEBUG',
                   dest='loglevel')
    p.add_argument('--profile', '-p',
                   default='ipad')
    p.add_argument('--keep', '-k',
                   action='store_true')
    p.add_argument('--wait',
                   action='store_true')

    p.add_argument('things', nargs='*')

    p.set_defaults(loglevel='WARNING')
    return p.parse_args()


def main():
    global active

    args = parse_args()
    logging.basicConfig(level=args.loglevel)

    active = []
    for thing in args.things:
        thing = Path(thing)
        torrent = {
            'torrent_dir': str(thing.parent),
            'torrent_name': str(thing.name),
        }

        r = tasks.process_torrent.delay(
            torrent=torrent,
            keep=args.keep,
            profile=args.profile)

        active.append(r)

if __name__ == '__main__':
    main()
