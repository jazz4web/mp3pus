import importlib.util

from ..system import check_dep, show_error

if importlib.util.find_spec('mutagen') is None:
    show_error('python3 module mutagen is not installed')

if check_dep('lame'):
    show_error('lame is not installed')

if check_dep('opusenc'):
    show_error('opus-tools is not installed')
