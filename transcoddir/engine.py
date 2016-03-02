from __future__ import absolute_import

import logging
import pkg_resources
import yaml
from pathlib2 import Path

from . import video

LOG = logging.getLogger(__name__)
PROFILES_PATH = pkg_resources.resource_filename(
    __name__, 'data/profiles.yml')
VIDEO_EXTENSIONS = set((
    '.mov,.mpg,.mp4,.avi,.wmf,.mkv,.ogg,.ogv,'
    '.m4v,.mpeg,.webm,.flv,.wmv,.asf'
).split(','))

with open(PROFILES_PATH) as fd:
    PROFILES = yaml.load(fd)


class Engine(object):
    def __init__(self, profile='default', keep=False):
        self.profile = PROFILES[profile]
        self.keep = keep

    def process_one_file(self, path):
        if path.suffix not in VIDEO_EXTENSIONS:
            LOG.info('skipped %s: not a video', path)
            return

        LOG.info('processing file %s', path)

        try:
            v = video.Video(path)
            v.transcode(profile=self.profile)
            if not self.keep:
                path.unlink()
        except video.VideoError as err:
            LOG.error('%s: transcoding failed: %s',
                      path, err)

    def process_files_in(self, path):
        LOG.info('processing files in %s', path)
        for item in path.iterdir():
            if item.is_dir():
                self.process_files_in(item)
                continue
            else:
                self.process_one_file(item)

    def process(self, path):
        path = Path(path)

        if path.is_dir():
            self.process_files_in(path)
        else:
            self.process_one_file(path)
