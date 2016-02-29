#!/usr/bin/python

import argparse
import json
import logging
import shutil
import subprocess
import time
from pathlib2 import Path

import video

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
    p.add_argument('--input-dir', '-i',
                   default='videos-in',
                   type=Path)
    p.add_argument('--output-dir', '-o',
                   default='videos-out',
                   type=Path)
    p.add_argument('--failed-dir', '-f',
                   default='videos-failed',
                   type=Path)
    p.add_argument('--create-dirs',
                   action='store_true')
    p.add_argument('--profile', '-p',
                   default='ipad')

    p.set_defaults(loglevel='WARNING')
    return p.parse_args()


def move_file(src, dest):
    LOG.debug('move %s to %s', src, dest)
    dest.parent.mkdir(mode=0o755,
                      parents=True,
                      exist_ok=True)
    shutil.move(str(src), str(dest))


def process_files_in(dir, args=None):
    LOG.info('processing files in %s', dir)
    for item in dir.iterdir():
        LOG.info('processing %s', item)
        if item.is_dir():
            process_files_in(item, args=args)
            try:
                item.rmdir()
                LOG.info('removed directory %s', item)
            except OSError:
                pass
            continue

        newpath = args.output_dir / item.relative_to(args.input_dir)
        try:
            v = video.Video(item)
            v.transcode(newpath.with_suffix('.m4v'),
                        create_dirs=True,
                        profile=video.profiles[args.profile])
            item.unlink()
        except video.TranscodingFailed:
            newpath = args.failed_dir / item.relative_to(args.input_dir)
            move_file(item, newpath)
        except video.NotAVideo:
            move_file(item, newpath)


def main():
    args = parse_args()
    logging.basicConfig(level=args.loglevel)

    if args.create_dirs:
        for dir in [args.input_dir, args.output_dir, args.failed_dir]:
            if not dir.is_dir():
                LOG.info('creating directory %s', dir)
                dir.mkdir(mode=0o755)

    process_files_in(args.input_dir, args=args)

if __name__ == '__main__':
    main()
