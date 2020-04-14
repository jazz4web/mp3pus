import shlex
import os


class Master:
    def __init__(self, opts):
        self.ini = shlex.split(opts or '')
        self.res = list()

    def _check_picture(self):
        if '--picture' in self.ini:
            spec = self.ini[self.ini.index('--picture') + 1]
            if '|' in spec:
                spec = spec.split('|')
                if len(spec) != 5 or \
                        not spec[0].isdecimal() or \
                        (int(spec[0]) < 0 or int(spec[0]) > 20) or \
                        not os.path.exists(spec[4]):
                    raise OSError('bad encoder options:picture_spec')
                spec[1], spec[3] = '', ''
                if ' ' in spec[2]:
                    spec[2] = "'" + spec[2] + "'"
                spec[4] = "'" + os.path.realpath(spec[4]) + "'"
                self.res.append('--picture')
                self.res.append('|'.join(spec))
            else:
                if not os.path.exists(spec):
                    raise OSError('bad encoder options:picture')
                self.res.append('--picture')
                self.res.append("'" + os.path.realpath(spec) + "'")

    def _check_bitrate(self):
        if '--bitrate' in self.ini:
            spec = self.ini[self.ini.index('--bitrate') + 1]
            if not spec.isdecimal() or \
                    (int(spec) < 16 or int(spec) > 256):
                raise OSError('bad encoder options:bitrate')
            self.res.append('--bitrate')
            self.res.append(spec)

    def check(self):
        self._check_bitrate()
        self._check_picture()
        if self.res:
            return ' '.join(self.res)
        return ''
