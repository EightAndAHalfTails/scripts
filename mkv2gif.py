#!/usr/bin/env python

"""Extract animated gifs from mkv files

Usage:
  mkv2gif.py [options] <input> <output>
  mkv2gif.py (-h | --help)
  mkv2gif.py --version

Options:
  -h --help            Show this screen.
  --version            Show version.
  --start=<pos>        Start position in HH:MM:SS format Default is 00:00:00
  --length=<len>       Length in seconds. Omit to keep going until the end.
  --resolution=<res>   Output resolution. Default is 640x360
  --fuzz=<fuz%>        Fuzz factor as percentage
  --subs=<track>       Subtitle Track. Omit for no subs

"""
from docopt import docopt
import os
import subprocess
from shlex import quote
from tempfile import mkdtemp
from shutil import rmtree

if __name__ == '__main__':
    arguments = docopt(__doc__, version='mkv2gif 0.1')
    print(arguments)
    
    tmpdir = mkdtemp()
    subs = os.path.join(tmpdir, "subs.ass")
    mp4 = os.path.join(tmpdir, "tmp.mp4")
    frames = os.path.join(tmpdir, arguments['<output>']+"%05d.gif")
    
    length = ''
    if arguments.get('--length') is not None:
        length = '-t ' + arguments.get('--length')

    start = ''
    if arguments.get('--start') is not None:
        start = '-ss ' + arguments.get('--start')

    res = '-s 640x360'
    if arguments.get('--resolution') is not None:
        res = '-s ' + arguments.get('--resolution')
            
    if(arguments['--subs']):
        command = "mkvextract tracks {} {}:{}".format(
            quote(arguments['<input>']),
            arguments['--subs'],
            subs)
        print("Extracting subs...")
        print('>'+command)
        subprocess.call(command, shell=True)

        command = "ffmpeg {} -i {} -strict -2 -sn -vcodec libx264 {} -vf ass={} {}".format(
            length,
            quote(arguments['<input>']),
            start,
            subs,
            mp4)
        print('>'+command)
        subprocess.call(command, shell=True)

        command = "ffmpeg -i {} {} {}".format(
            mp4,
            res,
            frames)
        print('>'+command)
        subprocess.call(command, shell=True)

    else:
        command = "ffmpeg {} {} -i {} {} {}".format(
            start,
            length,
            quote(arguments['<input>']),
            res,
            frames)
        print('>'+command)
        subprocess.call(command, shell=True)

    fuzz_factor=''
    if arguments['--fuzz'] is not None:
        fuzz_factor="-fuzz " + arguments['--fuzz']
    command = "convert -delay 5 -loop 0 {} -layers optimize-transparency {} {}.gif".format(
        fuzz_factor,
        os.path.join(tmpdir, arguments['<output>']+"*.gif"),
        arguments['<output>'])
    print('>'+command)
    subprocess.call(command, shell=True)

    rmtree(tmpdir)
