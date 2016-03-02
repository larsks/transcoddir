#!/usr/bin/python

import argparse
import yaml
import logging
import pkg_resources
from pathlib2 import Path

import video

LOG = logging.getLogger(__name__)
VIDEO_EXTENSIONS = (
    '.mov,.mpg,.mp4,.avi,.wmf,.mkv,.ogg,.ogv,'
    '.m4v,.mpeg,.webm,.flv,.wmv,.asf'
)


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
    p.add_argument('--profiles', '-P')
    p.add_argument('--profile', '-p',
                   default='ipad')
    p.add_argument('--video-extensions', '-V',
                   default=VIDEO_EXTENSIONS,
                   type=lambda ext: ext.split(','))
    p.add_argument('--keep', '-k',
                   action='store_true')

    p.add_argument('things', nargs='*')

    p.set_defaults(loglevel='WARNING')
    return p.parse_args()


def process_one_file(path):
    global args
    global profiles

    if path.suffix not in args.video_extensions:
        LOG.info('skipped %s: not a video', path)
        return

    LOG.info('processing file %s', path)

    try:
        v = video.Video(path)
        v.transcode(path.with_suffix('.m4v'),
                    profile=profiles[args.profile])
        if not args.keep:
            path.unlink()
    except video.VideoError as err:
        LOG.error('%s: transcoding failed: %s',
                  path, err)


def process_files_in(path):
    global args
    global profiles

    LOG.info('processing files in %s', path)
    for item in path.iterdir():
        if item.is_dir():
            process_files_in(item)
            continue
        else:
            process_one_file(item)


def main():
    global args
    global profiles

    args = parse_args()
    logging.basicConfig(level=args.loglevel)

    if args.profiles is None:
        args.profiles = pkg_resources.resource_filename(
            __name__, 'data/profiles.yml')

    with open(args.profiles) as fd:
        profiles = yaml.load(fd)

    for thing in (Path(x) for x in args.things):
        if thing.is_dir():
            process_files_in(thing)
        else:
            process_one_file(thing)

if __name__ == '__main__':
    main()
