#!/usr/bin/env python

"""Re-encode sections of mkvs to webm format

Usage:
  mkv2webm.py [options] <input> <output>
  mkv2webm.py (-h | --help)
  mkv2webm.py --version

Options:
  -h --help            Show this screen.
  --version            Show version.
  --start=<pos>        Start position in HH:MM:SS format Default is 00:00:00
  --length=<len>       Length in seconds. Omit to keep going until the end.
  --subs=<track>       Subtitle Track. Omit for no subs

"""
from docopt import docopt
import os
import subprocess
from shlex import quote

subs = "subs.ass"

def extractSubs(mkv_filename, subtitle_track):
    command = "mkvextract tracks {} {}:{}".format(
        quote(mkv_filename),
        subtitle_track,
        subs)
    print("Extracting subs...")
    print('>'+command)
    subprocess.call(command, shell=True)

def burnInSubs(mkv_filename, webm_filename, start, length):
    command = "ffmpeg -i {fin} -c:v libvpx -crf 4 -b:v 1500K -vf scale=640:-1 -an {st} {ln} -vf ass={ass} {fout}".format(
        st=start,
        ln=length,
        fin="file:"+quote(mkv_filename),
        ass=subs,
        fout=webm_filename)
    print("Burning in subs...")
    print('>'+command)
    subprocess.call(command, shell=True)

def reencode(mkv_filename, webm_filename, start='', length=''):
    
    command = "ffmpeg -i {} {} {} -c:v libvpx -crf 4 -b:v 1500K -vf scale=640:-1 -an {}".format(
        "file:"+quote(mkv_filename),
        start,
        length,
        webm_filename )
    print("Re-encoding...")
    print('>'+command)
    subprocess.call(command, shell=True)

if __name__ == '__main__':
    arguments = docopt(__doc__, version='mkv2webm 0.1')
    print(arguments)
    
    length = ''
    if arguments.get('--length') is not None:
        length = '-t ' + arguments.get('--length')

    start = ''
    if arguments.get('--start') is not None:
        start = '-ss ' + arguments.get('--start')

    mkv_in = arguments['<input>']
    webm_out = arguments['<output>']

    if arguments['--subs']:
        extractSubs(mkv_in, arguments['--subs'])
        burnInSubs(mkv_in, webm_out, start, length)
        os.remove(subs)
    else:
        reencode(mkv_in, webm_out, start, length)
