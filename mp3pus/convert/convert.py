import os
import shlex
import subprocess

from mutagen import mp3, MutagenError


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
        self.is_mp3 = None
        self.TMP = '/tmp/mp3pus.tmp.picture'
        self.picture = None

    def _get_key(self, item, tag, key):
        attr = item.get(tag)
        if attr:
            return ' {0} "{1}"'.format(key, attr.text[0])

    def _get_tracknum(self, item):
        track = item.get('TRCK')
        if track:
            track = track.text[0]
            if track and '/' in track:
                track = track.split('/')
                self.tracknumber = " --comment tracknumber={}".format(track[0])
                self.tracktotal = " --comment tracktotal={}".format(track[1])
            elif track and '/' not in track:
                self.tracknumber = " --comment tracknumber={}".format(track)

    def _get_comment(self, item):
        did = item.get('TXXX:DISCID')
        if did:
            self.comment = " --comment comment='{}'".format(
                did.desc + ': ' + did.text[0])
        comm = item.get('COMM::XXX')
        if comm:
            self.comment = " --comment comment='{}'".format(comm.text[0])

    def _get_picture(self, item):
        for key in item.keys():
            if 'APIC:' in key:
                pic = item.get(key)
                if pic and pic.type.real == 3:
                    f = open(self.TMP, 'wb')
                    f.write(pic.data)
                    f.close()
                    return " --picture 3||'front cover'||{}".format(
                        self.TMP)

    def get_metadata(self, picture=False):
        try:
            item = mp3.MP3(self.target)
            self.album = self._get_key(item, 'TALB', '--album')
            self.genre = self._get_key(item, 'TCON', '--genre')
            self.title = self._get_key(item, 'TIT2', '--title')
            self.artist = self._get_key(item, 'TPE1', '--artist')
            self.date = self._get_key(item, 'TDRC', '--date')
            self._get_tracknum(item)
            self._get_comment(item)
            self.is_mp3 = True
            if picture:
                self.picture = self._get_picture(item)
        except MutagenError:
            print(
                '{} is not mp3, passed'.format(os.path.basename(self.target)))

    def _get_lame(self):
        cmd = 'lame --silent --decode "{}" -'.format(self.target)
        return shlex.split(cmd)

    def _get_opus(self, options):
        cmd = 'opusenc {0}{1}{2}{3}{4}{5}{6}{7}{8}{9} - "{10}"'.format(
            options or '',
            self.album or '',
            self.genre or '',
            self.title or '',
            self.artist or '',
            self.tracknumber or '',
            self.tracktotal or '',
            self.date or '',
            self.comment or '',
            self.picture or '',
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
