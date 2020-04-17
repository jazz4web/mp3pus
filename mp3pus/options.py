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
                    not 16 <= float(spec) <= 256:
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

    def _check_comp(self):
        if '--comp' in self.ini:
            spec = self.ini[self.ini.index('--comp') + 1]
            if not spec.isdecimal() or not 0 <= int(spec) <= 10:
                raise OSError('bad encoder options:comp')
            self.res.append('--comp')
            self.res.append(spec)

    def _check_framesize(self):
        if '--framesize' in self.ini:
            spec = self.ini[self.ini.index('--framesize') + 1]
            if spec not in ('2.5', '5', '10', '20', '40', '60'):
                raise OSError('bad encoder options:framesize')
            self.res.append('--framesize')
            self.res.append(spec)

    def _check_max_delay(self):
        if '--max-delay' in self.ini:
            spec = self.ini[self.ini.index('--max-delay') + 1]
            if not spec.isdecimal() or not 0 <= int(spec) <= 1000:
                raise OSError('bad encoder options:max-delay')
            self.res.append('--max-delay')
            self.res.append(spec)

    def check(self):
        self._check_downmix()
        self._check_vbr()
        self._check_comp()
        self._check_framesize()
        self._check_bitrate()
        self._check_max_delay()
        self._check_picture()
        if self.res:
            return ' '.join(self.res)
        return ''
