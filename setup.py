from setuptools import setup, find_packages
from transcoddir import __version__

with open('requirements.txt') as fd:
    requires = fd.read().splitlines()

setup(name='transcoddir',
      author='Lars Kellogg-Stedman',
      author_email='lars@oddbit.com',
      url='https://github.com/larsks/transcoddir',
      version=__version__,
      packages=find_packages(),
      install_requires=requires,
      entry_points={
          'console_scripts': [
              'transcoddir = transcoddir.main:main',
              'transmission-torrent-done = transcoddir.transmission:torrent_done',
          ]})
