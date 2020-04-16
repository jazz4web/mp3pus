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

    @staticmethod
    def try_float(s):
        try:
            float(s)
        except ValueError:
            return False
        return True

    def _check_bitrate(self):
        if '--bitrate' in self.ini:
            spec = self.ini[self.ini.index('--bitrate') + 1]
            if not self.try_float(spec) or \
                    (float(spec) < 16 or float(spec) > 256):
                raise OSError('bad encoder options:bitrate')
            self.res.append('--bitrate')
            self.res.append(str(round(float(spec), 3)))

    def _check_downmix(self):
        if '--downmix-mono' in self.ini:
            self.res.append('--downmix-mono')

    def _check_vbr(self):
        if '--vbr' in self.ini:
            self.res.append('--vbr')
        if '--cvbr' in self.ini and '--vbr' not in self.res:
            self.res.append('--cvbr')
        if '--hard-cbr' in self.ini:
            if '--vbr' not in self.res and '--cvbr' not in self.res:
                self.res.append('--hard-cbr')

    def check(self):
        self._check_downmix()
        self._check_vbr()
        self._check_bitrate()
        self._check_picture()
        if self.res:
            return ' '.join(self.res)
        return ''
