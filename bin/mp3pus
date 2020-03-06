#!/usr/bin/env python3

import argparse
import glob
import os
import shlex
import subprocess

from mutagen import mp3


def parse_args():
    args = argparse.ArgumentParser()
    args.add_argument(
        '-v', '--version', action='version', version='mp3pus-1.0pre')
    args.add_argument(
        '-i',
        action='store',
        dest='input_dir',
        required=True,
        help='input directory')
    args.add_argument(
        '-d',
        action='store',
        dest='output_dir',
        required=True,
        help='output directory')
    args.add_argument(
        '-o',
        action='store',
        dest='enc_options',
        help='encoder options')
    return args.parse_args()


class Target:
    def __init__(self, filename, out_dir):
        self.target = filename
        self.opus = os.path.join(
            os.path.realpath(out_dir),
            os.path.splitext(os.path.basename(filename))[0]) + '.opus'
        self.album = None
        self.genre = None
        self.title = None
        self.artist = None
        self.date = None
        self.tracknumber = None
        self.tracktotal = None
        self.comment = None

    def get_metadata(self):
        item = mp3.MP3(self.target)
        if item.get('TALB'):
            self.album = " --album '{0}'".format(item.get('TALB').text[0])
        if item.get('TCON'):
            self.genre = " --genre '{}'".format(item.get('TCON').text[0])
        if item.get('TIT2'):
            self.title = " --title '{}'".format(item.get('TIT2').text[0])
        if item.get('TPE1'):
            self.artist = " --artist '{}'".format(item.get('TPE1').text[0])
        if item.get('TDRC'):
            self.date = " --date {}".format(item.get('TDRC').text[0])
        if item.get('TRCK'):
            track = item.get('TRCK').text[0]
            if track and '/' in track:
                track = track.split('/')
                self.tracknumber = " --comment tracknumber={}".format(track[0])
                self.tracktotal = " --comment tracktotal={}".format(track[1])
            elif track and '/' not in track:
                self.tracknumber = " --comment tracknumber={}".format(track)
        if item.get('TXXX:DISCID'):
            t = item.get('TXXX:DISCID')
            self.comment = " --comment comment='{}'" \
                .format(t.desc.lower() + ": " + t.text[0])
        if item.get('COMM::XXX'):
            self.comment = " --comment comment='{}'" \
                .format(item.get('COMM::XXX').text[0])

    def _get_lame(self):
        cmd = 'lame --silent --decode "{}" -'.format(self.target)
        return shlex.split(cmd)

    def _get_opus(self, options):
        cmd = 'opusenc {0}{1}{2}{3}{4}{5}{6}{7}{8} - "{9}"'.format(
            options or '',
            self.album or '',
            self.genre or '',
            self.title or '',
            self.artist or '',
            self.tracknumber or '',
            self.tracktotal or '',
            self.date or '',
            self.comment or '',
            self.opus)
        return shlex.split(cmd)

    def convert(self, options):
        with subprocess.Popen(
                self._get_lame(),
                stdout=subprocess.PIPE) as lame, \
                subprocess.Popen(
                    self._get_opus(options),
                    stderr=subprocess.PIPE,
                    stdin=lame.stdout) as opus:
            opus.wait()


if __name__ == '__main__':
    keys = parse_args()
    template = os.path.join(os.path.realpath(keys.input_dir), '*.mp3')
    for each in glob.glob(template):
        target = Target(each, keys.output_dir)
        target.get_metadata()
        target.convert(keys.enc_options)
        print(os.path.basename(target.target), end=' ')
        print('->', end=' ')
        print(os.path.basename(target.opus))
