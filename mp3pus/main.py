import argparse
import glob
import os


def parse_args(version):
    args = argparse.ArgumentParser()
    args.add_argument(
        '-v', '--version', action='version', version=version)
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
    args.add_argument(
        '-p',
        action='store_true',
        dest='picture',
        default=False,
        help='get the picture if there is one')
    return args.parse_args()


def start_the_process(arguments):
    if not os.path.exists(arguments.input_dir):
        raise OSError('{} does not exist'.format(arguments.input_dir))
    if not os.path.exists(arguments.output_dir):
        raise OSError('{} does not exist'.format(arguments.output_dir))
    from .options import Master
    cmd = Master(arguments.enc_options)
    template = os.path.join(os.path.realpath(arguments.input_dir), '*.mp3')
    from .convert.convert import Target
    target = None
    for each in sorted(glob.glob(template)):
        if not os.path.exists(each):
            print('{0} - not found, passed'.format(os.path.basename(each)))
        else:
            target = Target(each, arguments.output_dir)
            target.get_metadata(arguments.picture)
            if target.is_mp3:
                print(os.path.basename(target.target), end=' ')
                print('->', end=' ')
                print(os.path.basename(target.opus))
                target.convert(cmd.check())
    if target and os.path.exists(target.TMP):
        os.remove(target.TMP)
