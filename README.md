# Transcoddir

Transcoddir will transcode a single file or all files in a directory
tree into the specified format.

## Usage

Transcode a single file:

    transcoddir path/to/file.mp4

Transcode a directory:

    transcoddir path/to/directory/

Transcode multiple files:

    transcoddir file1.mp4 file2.mkv file3.avi

## Profiles

Transcoding profiles are specified as a YAML document.  The defaults
can be found in the `transcoddir/data/profiles.yml`, which defines
"ipad" and "ipad-small".

## License

transcoddir -- transcode a collection of videos  
Copyright (C) 2016 Lars Kellogg-Stedman <lars@oddbit.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

