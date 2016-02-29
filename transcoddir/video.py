import json
import subprocess
import logging

from pathlib2 import Path

LOG = logging.getLogger(__name__)


profiles = {
    'ipad': {
        'audio_codec': 'aac',
        'audio_args': ['-strict', '-2'],
        'video_codec': 'libx264',
        'height': 720,
        'width': 1280,
        'video_args': [
            '-profile:v', 'main',
            '-level', '3.1',
            '-preset', 'fast',
            '-crf', '23',
            '-x264-params', 'ref=4',
            '-movflags', '+faststart',
        ]
    },
    'ipad-small': {
        'audio_codec': 'aac',
        'audio_args': ['-strict', '-2'],
        'video_codec': 'libx264',
        'height': 480,
        'width': 852,
        'video_args': [
            '-profile:v', 'main',
            '-level', '3.1',
            '-preset', 'fast',
            '-crf', '23',
            '-x264-params', 'ref=4',
            '-movflags', '+faststart',
        ]
    },
}


class VideoError(Exception):
    pass


class NotAVideo(VideoError):
    pass


class TranscodingFailed(VideoError):
    pass


class Video(object):
    def __init__(self, path):
        self.path = Path(path)
        self.get_info()

        # *that's* not a video format we care about
        if self._format['format_name'] == 'tty':
            raise NotAVideo(self.path)

    def get_info(self):
        try:
            res = json.loads(subprocess.check_output(
                ['ffprobe',
                 '-show_streams', '-show_format',
                 '-hide_banner',
                 '-print_format', 'json', str(self.path)]))
        except subprocess.CalledProcessError:
            raise NotAVideo(self.path)

        self._streams = res.get('streams')
        self._format = res.get('format')

    def __str__(self):
        return '<%s (%s)>' % (
            self.path,
            self._format['format_long_name'])

    def stream_types(self):
        return [(s['codec_type'], s['codec_name']) for s in self._streams]

    def audio_codec(self):
        '''Returns the codec of the first audio stream'''
        return [s[1] for s in self.stream_types()
                if s[0] == 'audio'][0]

    def video_codec(self):
        '''Returns the codec of the first video stream'''
        return [s[1] for s in self.stream_types()
                if s[0] == 'video'][0]

    def video_size(self):
        stream = [s for s in self._streams if s['codec_type'] == 'video'][0]
        return (stream['width'], stream['height'])

    def transcode(self, output,
                  video_codec=None, video_args=None,
                  audio_codec=None, audio_args=None,
                  height=None, width=None, scale=True,
                  profile=None, loglevel='warning',
                  create_dirs=False, dir_mode=0o755,
                  copy_if_same=False):

        output = Path(output)

        if create_dirs:
            output.parent.mkdir(mode=dir_mode, parents=True,
                                exist_ok=True)

        cmd = [
            'ffmpeg',
            '-loglevel', loglevel, '-hide_banner', '-nostats',
            '-y',
            '-i', str(self.path)
        ]

        if profile is None:
            profile = {
                'video_codec': 'copy',
                'audio_codec': 'copy',
            }

        if video_codec is not None:
            profile['video_codec'] = video_codec

        if video_args is not None:
            profile['video_args'] = video_args

        if audio_codec is not None:
            profile['audio_codec'] = audio_codec

        if audio_args is not None:
            profile['audio_args'] = audio_args

        if height is not None:
            profile['height'] = height

        if width is not None:
            profile['width'] = width

        if copy_if_same and profile['video_codec'] == self.video_codec():
            profile['video_codec'] = 'copy'

        if copy_if_same and profile['audio_codec'] == self.audio_codec():
            profile['audio_codec'] = 'copy'

        if scale and ((profile['width'], profile['height'])
                      != self.video_size()):
            if profile['video_codec'] == 'copy':
                raise ValueError('cannot resize with "copy" codec')

            # why -2? https://trac.ffmpeg.org/ticket/309
            cmd += ['-vf', 'scale=%d:-2' % profile['width']]

        cmd += ['-c:a', profile['audio_codec']]
        if profile.get('audio_args'):
            cmd += profile['audio_args']

        cmd += ['-c:v', profile['video_codec']]
        if profile.get('video_args'):
            cmd += profile['video_args']

        cmd += [str(output)]

        LOG.debug('running %s', cmd)

        try:
            subprocess.check_call(cmd)
        except subprocess.CalledProcessError:
            LOG.error('%s: transcoding failed: removing output file "%s"',
                      self.path, output)
            try:
                output.unlink()
            except OSError:
                pass

            raise TranscodingFailed(self.path)
        except KeyboardInterrupt:
            LOG.error('%s: transcoding interrupted by user: '
                      'removing output file "%s"',
                      self.path, output)
            try:
                output.unlink()
            except OSError:
                pass

            raise


if __name__ == '__main__':
    import sys

    logging.basicConfig(level='DEBUG')
    v = Video(sys.argv[1])
